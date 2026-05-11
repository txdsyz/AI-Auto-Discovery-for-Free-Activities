"""
Firebase Firestore Client
Handles database operations
"""
import firebase_admin
from firebase_admin import credentials, firestore
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
from app.config import settings


# Global flag to track if Firebase has been initialized
_firebase_initialized = False


class FirestoreClient:
    """Client for Firebase Firestore database operations"""
    
    def __init__(self):
        """Initialize Firebase Admin SDK"""
        global _firebase_initialized
        
        # Only initialize Firebase once
        if not _firebase_initialized:
            # Get absolute path to credentials
            creds_path = settings.FIREBASE_CREDENTIALS_PATH
            if not Path(creds_path).is_absolute():
                creds_path = Path(__file__).parent.parent.parent / creds_path
            
            try:
                # Initialize Firebase app
                cred = credentials.Certificate(str(creds_path))
                firebase_admin.initialize_app(cred)
                _firebase_initialized = True
                print("✓ Firebase initialized successfully")
            except Exception as e:
                print(f"✗ Firebase initialization failed: {str(e)}")
                raise
        
        # Get Firestore client (can be called multiple times safely)
        self.db = firestore.client()
    
    # Organizations
    
    def add_organization(self, data: Dict[str, Any]) -> str:
        """
        Add a new organization to Firestore.
        
        Args:
            data: Organization data dictionary
            
        Returns:
            Document ID of the created organization
        """
        doc_ref = self.db.collection('organizations').document()
        doc_ref.set(data)
        return doc_ref.id
    
    def save_organization_with_events(self, profile: Dict[str, Any]) -> Dict[str, str]:
        """
        Save organization profile with all events and metadata.
        
        This method:
        1. Checks for duplicates (by URL)
        2. Saves organization with discovery metadata
        3. Saves all events as separate documents
        4. Links events to organization
        
        Args:
            profile: Complete organization profile from profiling service
            
        Returns:
            Dict with org_id and list of event_ids
            
        Example:
            result = await save_organization_with_events(profile)
            # Returns: {"org_id": "abc123", "event_ids": ["evt1", "evt2"]}"
        """
        # Check for duplicate
        existing = self.get_organization_by_url(profile['website'])
        if existing:
            print(f"⚠️  Organization already exists: {existing['name']} (ID: {existing['id']})")
            print(f"   Updating instead of creating new...")
            
            # Update existing organization
            org_id = existing['id']
            update_data = {
                'last_updated': datetime.utcnow().isoformat(),
                'contact': profile.get('contact', {}),
                'description': profile.get('description'),
                'location': profile.get('location'),
            }
            
            # Update discovery metadata if new one provided
            if 'discovery' in profile:
                update_data['discovery'] = profile['discovery']
            
            self.db.collection('organizations').document(org_id).update(update_data)
        else:
            # Create new organization
            org_data = {
                'name': profile['name'],
                'type': profile['type'],
                'website': profile['website'],
                'contact': profile.get('contact', {}),
                'location': profile.get('location'),
                'description': profile.get('description'),
                'status': 'pending',  # Default status for new organizations
                'created_at': profile.get('created_at', datetime.utcnow().isoformat()),
                'last_updated': profile.get('last_updated', datetime.utcnow().isoformat()),
                # Discovery metadata - how we found this org
                'discovery': profile.get('discovery', {}),
            }
            
            org_id = self.add_organization(org_data)
            print(f"✅ Saved organization: {profile['name']} (ID: {org_id})")
        
        # Save events
        event_ids = []
        events = profile.get('events', [])
        
        for event_data in events:
            event_doc = {
                'organization_id': org_id,
                'name': event_data['name'],
                'type': event_data.get('type'),
                'schedule': event_data.get('schedule'),
                'date': event_data.get('date'),
                'age_range': event_data.get('age_range'),
                'description': event_data.get('description'),
                'created_at': datetime.utcnow().isoformat(),
            }
            
            event_id = self.add_event(event_doc)
            event_ids.append(event_id)
        
        print(f"✅ Saved {len(event_ids)} events for {profile['name']}")
        
        return {
            'org_id': org_id,
            'event_ids': event_ids
        }
    
    def get_organization(self, org_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a single organization by ID.
        
        Args:
            org_id: Organization document ID
            
        Returns:
            Organization data dictionary or None if not found
        """
        doc_ref = self.db.collection('organizations').document(org_id)
        doc = doc_ref.get()
        
        if doc.exists:
            data = doc.to_dict()
            data['id'] = doc.id
            return data
        return None
    
    def get_organization_by_url(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Get organization by website URL (for deduplication).
        
        This is CRITICAL for cost savings - prevents re-scraping same organizations.
        
        Args:
            url: Organization website URL
            
        Returns:
            Organization data dictionary or None if not found
        """
        query = self.db.collection('organizations').where('website', '==', url).limit(1)
        docs = list(query.stream())
        
        if docs:
            data = docs[0].to_dict()
            data['id'] = docs[0].id
            return data
        return None
    
    def get_all_organizations(
        self,
        limit: int = 10,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get all organizations with pagination.
        
        Args:
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            List of organization dictionaries
        """
        query = (
            self.db.collection('organizations')
            .order_by('created_at', direction=firestore.Query.DESCENDING)
            .limit(limit)
            .offset(offset)
        )
        
        docs = query.stream()
        organizations = []
        
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            organizations.append(data)
        
        return organizations
    
    def count_organizations(self) -> int:
        """Get total count of organizations"""
        # Note: For large collections, consider using aggregation queries
        docs = self.db.collection('organizations').stream()
        return len(list(docs))
    
    def update_organization_status(self, org_id: str, status: str) -> bool:
        """
        Update the status of an organization.
        
        Args:
            org_id: Organization document ID
            status: New status value (pending, background_check, onboarded, archived)
            
        Returns:
            True if updated successfully, False otherwise
        """
        try:
            self.db.collection('organizations').document(org_id).update({
                'status': status,
                'last_updated': datetime.utcnow().isoformat()
            })
            return True
        except Exception as e:
            print(f"Error updating organization status: {e}")
            return False
    
    def backfill_organization_status(self) -> Dict[str, int]:
        """
        Backfill 'status' field for all organizations that don't have it.
        Sets default status to 'pending'.
        
        Returns:
            Dictionary with counts of updated and skipped organizations
        """
        updated = 0
        skipped = 0
        
        docs = self.db.collection('organizations').stream()
        
        for doc in docs:
            data = doc.to_dict()
            if 'status' not in data:
                self.db.collection('organizations').document(doc.id).update({
                    'status': 'pending',
                    'last_updated': datetime.utcnow().isoformat()
                })
                updated += 1
                print(f"✅ Updated {data.get('name', 'Unknown')} to 'pending' status")
            else:
                skipped += 1
        
        return {'updated': updated, 'skipped': skipped}
    
    # Events
    
    def add_event(self, data: Dict[str, Any]) -> str:
        """
        Add a new event to Firestore.
        
        Args:
            data: Event data dictionary (must include organization_id)
            
        Returns:
            Document ID of the created event
        """
        doc_ref = self.db.collection('events').document()
        doc_ref.set(data)
        return doc_ref.id
    
    def get_events_by_org(self, org_id: str) -> List[Dict[str, Any]]:
        """
        Get all events for a specific organization.
        
        Args:
            org_id: Organization document ID
            
        Returns:
            List of event dictionaries
        """
        # Simple query without order_by to avoid requiring composite index
        query = self.db.collection('events').where('organization_id', '==', org_id)
        
        docs = query.stream()
        events = []
        
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            events.append(data)
        
        # Sort in Python instead of Firestore to avoid composite index requirement
        events.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return events
    
    # Discovery Runs
    
    def create_discovery_run(self, data: Dict[str, Any]) -> str:
        """
        Create a new discovery run document.
        
        Args:
            data: Discovery run data
            
        Returns:
            Document ID of the created run
        """
        doc_ref = self.db.collection('discovery_runs').document()
        doc_ref.set(data)
        return doc_ref.id
    
    def update_discovery_run(self, run_id: str, data: Dict[str, Any]):
        """
        Update a discovery run document.
        
        Args:
            run_id: Discovery run document ID
            data: Fields to update
        """
        doc_ref = self.db.collection('discovery_runs').document(run_id)
        doc_ref.update(data)
    
    def get_discovery_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a discovery run by ID.
        
        Args:
            run_id: Discovery run document ID
            
        Returns:
            Discovery run data or None if not found
        """
        doc_ref = self.db.collection('discovery_runs').document(run_id)
        doc = doc_ref.get()
        
        if doc.exists:
            data = doc.to_dict()
            data['id'] = doc.id
            return data
        return None
    
    # Standalone Events Methods
    
    def save_event(self, event_data: Dict[str, Any]) -> str:
        """
        Save a standalone event to Firestore.
        
        Args:
            event_data: Event data including title, sport_category, date, time, etc.
            
        Returns:
            Document ID of the saved event
        """
        # Add timestamps
        event_data['created_at'] = datetime.utcnow()
        event_data['last_updated'] = datetime.utcnow()
        
        # Add default status if not present
        if 'status' not in event_data:
            event_data['status'] = 'pending'
        
        # Add to Firestore
        doc_ref = self.db.collection('standalone_events').document()
        event_data['id'] = doc_ref.id
        doc_ref.set(event_data)
        
        print(f"✓ Saved event: {event_data.get('title')} (ID: {doc_ref.id})")
        return doc_ref.id
    
    def get_events(
        self,
        city: Optional[str] = None,
        status: Optional[str] = None,
        sport_category: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get events with optional filtering.
        
        Args:
            city: Filter by city name
            status: Filter by status (pending, verified, archived)
            sport_category: Filter by sport category
            date_from: Filter events from this date (YYYY-MM-DD)
            date_to: Filter events until this date (YYYY-MM-DD)
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            List of event dictionaries
        """
        query = self.db.collection('standalone_events')
        
        # Apply filters
        if city:
            query = query.where('city', '==', city)
        
        if status:
            query = query.where('status', '==', status)
        
        if sport_category:
            query = query.where('sport_category', '==', sport_category)
        
        if date_from:
            query = query.where('date', '>=', date_from)
        
        if date_to:
            query = query.where('date', '<=', date_to)
        
        # Only order by created_at if no filters (to avoid composite index requirement)
        # When filters are applied, fetch all and sort in memory
        if not (city or status or sport_category or date_from or date_to):
            query = query.order_by('created_at', direction=firestore.Query.DESCENDING)
        
        # Apply pagination
        query = query.limit(limit).offset(offset)
        
        # Execute query
        docs = query.stream()
        
        events = []
        for doc in docs:
            event_data = doc.to_dict()
            event_data['id'] = doc.id
            
            # Ensure status field exists (for backwards compatibility)
            if 'status' not in event_data:
                event_data['status'] = 'pending'
            
            events.append(event_data)
        
        return events
    
    def get_event_by_id(self, event_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a single event by ID.
        
        Args:
            event_id: Event document ID
            
        Returns:
            Event data or None if not found
        """
        doc_ref = self.db.collection('standalone_events').document(event_id)
        doc = doc_ref.get()
        
        if doc.exists:
            event_data = doc.to_dict()
            event_data['id'] = doc.id
            
            # Ensure status field exists
            if 'status' not in event_data:
                event_data['status'] = 'pending'
            
            return event_data
        
        return None
    
    def update_event_status(self, event_id: str, status: str) -> bool:
        """
        Update the status of an event.
        
        Args:
            event_id: Event document ID
            status: New status ('pending', 'verified', 'archived')
            
        Returns:
            True if successful, False if event not found
        """
        doc_ref = self.db.collection('standalone_events').document(event_id)
        
        # Check if event exists
        if not doc_ref.get().exists:
            return False
        
        # Update status and last_updated timestamp
        doc_ref.update({
            'status': status,
            'last_updated': datetime.utcnow()
        })
        
        print(f"✓ Updated event {event_id} status to: {status}")
        return True
    
    def delete_event(self, event_id: str) -> bool:
        """
        Delete an event from Firestore.
        
        Args:
            event_id: Event document ID
            
        Returns:
            True if successful, False if event not found
        """
        doc_ref = self.db.collection('standalone_events').document(event_id)
        
        # Check if event exists
        if not doc_ref.get().exists:
            return False
        
        doc_ref.delete()
        print(f"✓ Deleted event: {event_id}")
        return True
    
    def get_events_count(
        self,
        city: Optional[str] = None,
        status: Optional[str] = None
    ) -> int:
        """
        Get total count of events with optional filtering.
        
        Args:
            city: Filter by city name
            status: Filter by status
            
        Returns:
            Total count of events
        """
        query = self.db.collection('standalone_events')
        
        if city:
            query = query.where('city', '==', city)
        
        if status:
            query = query.where('status', '==', status)
        
        docs = query.stream()
        return len(list(docs))


# Create global client instance (will be initialized when first imported)
firestore_client = FirestoreClient()
