"""
Complete Discovery Pipeline Orchestration
Coordinates Stage 1 (Discovery) and Stage 2 (Profiling)
"""
from typing import List, Dict, Any
from datetime import datetime
import time
# from app.services.discovery import discover_organizations
# from app.services.profiling import profile_organization
# from app.integrations.firebase import firestore_client
from app.config import settings


async def run_discovery_pipeline(
    categories: List[str],
    max_orgs: int = 3
) -> Dict[str, Any]:
    """
    Execute the complete discovery pipeline.
    
    Steps:
    1. Create discovery run document in Firestore
    2. Stage 1: Discover organization URLs from web search
    3. Stage 2: Profile each organization (extract + LLM analysis)
    4. Save organizations and events to Firestore
    5. Update discovery run status
    6. Return results
    
    Args:
        categories: List of category names to search
        max_orgs: Maximum number of organizations to discover
        
    Returns:
        Dictionary with run_id, status, organizations, and metrics
        
    Example:
        result = await run_discovery_pipeline(
            categories=["sports", "youth_centers"],
            max_orgs=3
        )
    """
    start_time = time.time()
    
    # Prepare search queries for logging
    search_queries = [
        settings.CATEGORY_QUERIES.get(cat, cat)
        for cat in categories
    ]
    
    # TODO: Create discovery run document
    # run_doc = {
    #     "search_queries": search_queries,
    #     "status": "in_progress",
    #     "started_at": datetime.utcnow(),
    #     "organizations_found": 0,
    #     "total_events_extracted": 0
    # }
    # run_id = await firestore_client.create_discovery_run(run_doc)
    
    run_id = "placeholder_run_id"  # Remove when implementing
    
    print(f"Started discovery run: {run_id}")
    print(f"Categories: {categories}")
    print(f"Max organizations: {max_orgs}")
    
    try:
        # STAGE 1: Discover organizations
        print("\n=== STAGE 1: DISCOVERY ===")
        # org_urls = await discover_organizations(categories, max_orgs)
        org_urls = []  # Placeholder
        
        if not org_urls:
            raise ValueError("No organizations discovered")
        
        print(f"Discovered {len(org_urls)} organizations")
        
        # STAGE 2: Profile each organization
        print("\n=== STAGE 2: PROFILING ===")
        organizations = []
        errors = []
        
        for i, url in enumerate(org_urls, 1):
            print(f"\nProfiling {i}/{len(org_urls)}: {url}")
            
            try:
                # TODO: Profile organization
                # profile = await profile_organization(url)
                
                # TODO: Save to Firestore
                # org_id = await firestore_client.add_organization({
                #     "name": profile['name'],
                #     "type": profile['type'],
                #     "website": profile['website'],
                #     "contact": profile['contact'],
                #     "location": profile['location'],
                #     "description": profile['description'],
                #     "created_at": profile['created_at'],
                #     "last_updated": profile['last_updated']
                # })
                
                # TODO: Save events
                # for event in profile['events']:
                #     await firestore_client.add_event({
                #         "organization_id": org_id,
                #         "name": event['name'],
                #         "type": event['type'],
                #         "schedule": event.get('schedule'),
                #         "date": event.get('date'),
                #         "age_range": event['age_range'],
                #         "description": event['description'],
                #         "created_at": datetime.utcnow()
                #     })
                
                # profile['id'] = org_id
                # organizations.append(profile)
                
                pass  # Remove when implementing
                
            except Exception as e:
                error_msg = f"Error profiling {url}: {str(e)}"
                print(f"✗ {error_msg}")
                errors.append({
                    "url": url,
                    "stage": "profiling",
                    "error": str(e)
                })
                continue
        
        # Calculate totals
        total_events = sum(len(org.get('events', [])) for org in organizations)
        execution_time = time.time() - start_time
        
        # TODO: Update discovery run status
        # await firestore_client.update_discovery_run(run_id, {
        #     "status": "completed",
        #     "organizations_found": len(organizations),
        #     "total_events_extracted": total_events,
        #     "completed_at": datetime.utcnow()
        # })
        
        print("\n=== PIPELINE COMPLETED ===")
        print(f"Organizations found: {len(organizations)}")
        print(f"Total events: {total_events}")
        print(f"Execution time: {execution_time:.2f}s")
        print(f"Errors: {len(errors)}")
        
        return {
            "run_id": run_id,
            "status": "completed",
            "organizations": organizations,
            "total_organizations": len(organizations),
            "total_events": total_events,
            "execution_time_seconds": execution_time,
            "errors": errors
        }
        
    except Exception as e:
        # TODO: Update run as failed
        # await firestore_client.update_discovery_run(run_id, {
        #     "status": "failed",
        #     "error": str(e),
        #     "completed_at": datetime.utcnow()
        # })
        
        print(f"\n✗ Pipeline failed: {str(e)}")
        raise
