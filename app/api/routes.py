"""
API route handlers
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List
from .models import (
    DiscoverRequest,
    DiscoverResponse,
    Organization,
    OrganizationsListResponse,
    DiscoveryRunStatus,
    StatusUpdateRequest,
    # Event models (not imported here to avoid circular dependency, imported in route functions)
)
from app.services.discovery import discover_organizations as discover_orgs_service
from app.services.profiling import profile_organization
from app.integrations.firebase import FirestoreClient

router = APIRouter()

# Initialize Firebase client
firestore_client = FirestoreClient()


@router.post("/discover", response_model=DiscoverResponse)
async def discover_organizations(request: DiscoverRequest):
    """
    Run the discovery pipeline to find and profile youth organizations.
    
    This endpoint:
    1. Searches for organizations based on categories
    2. Extracts and profiles each organization's website
    3. Stores results in Firebase
    4. Returns structured organization data with events
    
    Frontend usage:
    ```javascript
    const response = await fetch('http://localhost:8000/discover', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        categories: ['sports', 'youth_centers'],
        max_organizations: 5
      })
    });
    const result = await response.json();
    console.log(`Found ${result.organizations_found} organizations`);
    ```
    """
    from datetime import datetime
    import uuid
    
    try:
        # Generate run ID
        run_id = f"run_{uuid.uuid4().hex[:12]}"
        started_at = datetime.now().isoformat()
        
        # Stage 1: Discovery
        print(f"[Discovery] Starting pipeline run {run_id}")
        print(f"Search query: '{request.search_query}', Max orgs: {request.max_organizations}")
        
        discovered_urls = await discover_orgs_service(
            search_query=request.search_query,
            max_orgs=request.max_organizations
        )
        
        print(f"[Discovery] Found {len(discovered_urls)} organizations")
        
        # Stage 2: Profiling + Storage
        organizations_saved = 0
        irrelevant_filtered = 0
        
        for org_data in discovered_urls:
            url = org_data['url']
            metadata = {
                'category': org_data['category'],
                'search_query': org_data['search_query'],
                'search_score': org_data['search_score'],
                'discovered_at': org_data['discovered_at']
            }
            
            print(f"\n[Profiling] Processing: {url}")
            print(f"  Category: {metadata['category']}")
            print(f"  Query: {metadata['search_query']}")
            
            # Profile organization
            try:
                profile = await profile_organization(url, discovery_metadata=metadata)
            except ValueError as val_error:
                # Check if it's an irrelevant organization
                if "IRRELEVANT:" in str(val_error):
                    print(f"  ⏭️  Filtered: {str(val_error)}")
                    irrelevant_filtered += 1
                else:
                    print(f"  ❌ Validation failed: {str(val_error)}")
                    irrelevant_filtered += 1
                continue
            except Exception as prof_error:
                print(f"  ❌ Failed to profile: {str(prof_error)}")
                irrelevant_filtered += 1
                continue
            
            # Save to Firebase
            save_result = firestore_client.save_organization_with_events(profile)
            org_id = save_result['org_id']
            event_ids = save_result['event_ids']
            
            print(f"  ✅ Saved: {profile['name']}")
            print(f"     Org ID: {org_id}")
            print(f"     Events: {len(event_ids)}")
            
            organizations_saved += 1
        
        completed_at = datetime.now().isoformat()
        
        # Return summary
        return {
            "run_id": run_id,
            "status": "completed",
            "organizations_found": len(discovered_urls),
            "organizations_saved": organizations_saved,
            "irrelevant_filtered": irrelevant_filtered,
            "started_at": started_at,
            "completed_at": completed_at
        }
        
    except Exception as e:
        import traceback
        print(f"❌ Error in discovery pipeline: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/organizations", response_model=OrganizationsListResponse)
async def get_organizations(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    category: str = Query(default=None, description="Filter by category (sports, youth_centers, scouts, cultural)"),
    status: str = Query(default=None, description="Filter by status (pending, background_check, onboarded, archived)")
):
    """
    Get all discovered organizations with pagination and filtering.
    
    Frontend usage:
    ```javascript
    // Get all organizations
    const response = await fetch('http://localhost:8000/organizations?limit=10&offset=0');
    const data = await response.json();
    
    // Filter by category
    const sports = await fetch('http://localhost:8000/organizations?category=sports');
    
    // Filter by status
    const pending = await fetch('http://localhost:8000/organizations?status=pending');
    ```
    """
    try:
        # Get organizations from Firestore
        orgs = firestore_client.get_all_organizations(limit, offset)
        
        # Load events for each organization
        for org in orgs:
            events = firestore_client.get_events_by_org(org['id'])
            org['events'] = events
            # Ensure status field exists with default 'pending'
            if 'status' not in org:
                org['status'] = 'pending'
        
        # Filter by category if provided
        if category:
            orgs = [
                org for org in orgs 
                if org.get('discovery', {}).get('category') == category
            ]
        
        # Filter by status if provided
        if status:
            orgs = [
                org for org in orgs
                if org.get('status', 'pending') == status
            ]
        
        total = firestore_client.count_organizations()
        
        return {
            "organizations": orgs,
            "total": total,
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/organizations/{org_id}", response_model=Organization)
async def get_organization(org_id: str):
    """
    Get a specific organization by ID with all its events.
    
    Frontend usage:
    ```javascript
    const response = await fetch('http://localhost:8000/organizations/abc123');
    const org = await response.json();
    console.log(org.name, org.events);
    ```
    """
    try:
        # Get organization from Firestore
        org = firestore_client.get_organization(org_id)
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")
        
        # Get all events for this organization
        events = firestore_client.get_events_by_org(org_id)
        org["events"] = events
        
        return org
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/organizations/{org_id}/status")
async def update_organization_status(org_id: str, request: StatusUpdateRequest):
    """
    Update the status of an organization.
    
    Frontend usage:
    ```javascript
    const response = await fetch('http://localhost:8000/organizations/abc123/status', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: 'onboarded' })
    });
    const result = await response.json();
    ```
    """
    try:
        # Check if organization exists
        org = firestore_client.get_organization(org_id)
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")
        
        # Update status
        success = firestore_client.update_organization_status(org_id, request.status)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update status")
        
        return {
            "success": True,
            "organization_id": org_id,
            "new_status": request.status,
            "message": f"Organization status updated to {request.status}"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/discover/{run_id}", response_model=DiscoveryRunStatus)
async def get_discovery_run_status(run_id: str):
    """
    Get the status of a discovery pipeline run.
    """
    try:
        # TODO: Implement Firestore query
        # run = await firestore_client.get_discovery_run(run_id)
        # if not run:
        #     raise HTTPException(status_code=404, detail="Discovery run not found")
        # return run
        
        raise HTTPException(
            status_code=501,
            detail="Firestore integration not yet implemented. Complete Phase 2.4 first."
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# STANDALONE EVENTS ENDPOINTS
# ============================================================================

@router.post("/events/discover")
async def discover_events(request: dict):
    """
    Discover free youth sports events for a specific city.
    
    Request body:
    {
        "city": "Uppsala",
        "max_events": 10
    }
    
    Returns discovery results with events found and saved.
    """
    from app.services.event_discovery import discover_events_for_city
    from app.api.models import EventDiscoveryRequest
    
    try:
        # Validate request
        discovery_request = EventDiscoveryRequest(**request)
        
        # Run discovery
        result = discover_events_for_city(
            city=discovery_request.city,
            max_events=discovery_request.max_events
        )
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/events")
async def get_events(
    city: str = Query(None, description="Filter by city"),
    status: str = Query(None, description="Filter by status (pending, verified, archived)"),
    sport_category: str = Query(None, description="Filter by sport category"),
    date_from: str = Query(None, description="Filter events from date (YYYY-MM-DD)"),
    date_to: str = Query(None, description="Filter events until date (YYYY-MM-DD)"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    """
    Get list of standalone events with optional filtering.
    
    Query parameters:
    - city: Filter by city name
    - status: pending, verified, or archived
    - sport_category: basketball, soccer, swimming, etc.
    - date_from: Start date (YYYY-MM-DD)
    - date_to: End date (YYYY-MM-DD)
    - limit: Max results (default 100)
    - offset: Pagination offset (default 0)
    """
    try:
        events = firestore_client.get_events(
            city=city,
            status=status,
            sport_category=sport_category,
            date_from=date_from,
            date_to=date_to,
            limit=limit,
            offset=offset
        )
        
        # Get total count
        total = firestore_client.get_events_count(city=city, status=status)
        
        return {
            "events": events,
            "total": total,
            "limit": limit,
            "offset": offset
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/events/{event_id}")
async def get_event(event_id: str):
    """
    Get a single event by ID.
    """
    try:
        event = firestore_client.get_event_by_id(event_id)
        
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        return event
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/events/{event_id}/status")
async def update_event_status(event_id: str, request: dict):
    """
    Update the status of an event.
    
    Request body:
    {
        "status": "verified"  // pending, verified, or archived
    }
    """
    from app.api.models import EventStatusUpdateRequest
    
    try:
        # Validate request
        status_request = EventStatusUpdateRequest(**request)
        
        # Check if event exists and update
        success = firestore_client.update_event_status(event_id, status_request.status)
        
        if not success:
            raise HTTPException(status_code=404, detail="Event not found")
        
        return {
            "success": True,
            "event_id": event_id,
            "new_status": status_request.status,
            "message": f"Event status updated to {status_request.status}"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/events/{event_id}")
async def delete_event(event_id: str):
    """
    Delete an event.
    """
    try:
        success = firestore_client.delete_event(event_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Event not found")
        
        return {
            "success": True,
            "event_id": event_id,
            "message": "Event deleted successfully"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
