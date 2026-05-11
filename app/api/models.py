"""
Pydantic models for API requests and responses
"""
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime


# Request Models

class DiscoverRequest(BaseModel):
    """Request model for discovery pipeline"""
    search_query: str = Field(
        description="Custom search query in Swedish (e.g., 'Södermalm idrottsförening ungdom')"
    )
    max_organizations: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Maximum number of organizations to discover"
    )


class StatusUpdateRequest(BaseModel):
    """Request model for updating organization status"""
    status: Literal['pending', 'background_check', 'onboarded', 'archived'] = Field(
        description="New status for the organization"
    )


# Response Models

class ContactInfo(BaseModel):
    """Contact information for an organization"""
    email: Optional[str] = None
    phone: Optional[str] = None


class DiscoveryMetadata(BaseModel):
    """Discovery metadata for an organization"""
    category: str  # sports, youth_centers, scouts, cultural
    search_query: str
    search_score: Optional[float] = None
    discovered_at: Optional[str] = None


class Event(BaseModel):
    """Event or program offered by an organization"""
    id: str
    name: str
    type: str  # "recurring" or "one-time"
    schedule: Optional[str] = None
    date: Optional[str] = None
    age_range: Optional[str] = None
    description: str
    created_at: Optional[datetime] = None


class Organization(BaseModel):
    """Organization profile"""
    id: str
    name: str
    type: str
    website: str
    contact: ContactInfo
    location: Optional[str] = None
    description: str
    discovery: DiscoveryMetadata
    status: Literal['pending', 'background_check', 'onboarded', 'archived'] = 'pending'
    events: List[Event] = []
    created_at: Optional[datetime] = None
    last_updated: Optional[datetime] = None


class DiscoverResponse(BaseModel):
    """Response from discovery pipeline"""
    run_id: str
    status: str
    organizations_found: int
    organizations_saved: int
    irrelevant_filtered: int
    started_at: str
    completed_at: str


class OrganizationsListResponse(BaseModel):
    """Response for list of organizations"""
    organizations: List[Organization]
    total: int
    limit: int
    offset: int


class DiscoveryRunStatus(BaseModel):
    """Status of a discovery run"""
    run_id: str
    status: str
    search_queries: List[str] = []
    organizations_found: Optional[int] = None
    total_events_extracted: Optional[int] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    error: Optional[str] = None


# Standalone Events Models

class StandaloneEvent(BaseModel):
    """Standalone event (not tied to an organization)"""
    id: str
    title: str
    sport_category: str
    date: Optional[str] = None  # YYYY-MM-DD format
    time: Optional[str] = None  # HH:MM format
    location: str
    age_group: str
    is_free: bool = True
    summary: str
    language: str  # "en" or "sv"
    source_url: str
    city: str
    status: Literal['pending', 'verified', 'archived'] = 'pending'
    created_at: Optional[datetime] = None
    last_updated: Optional[datetime] = None


class EventDiscoveryRequest(BaseModel):
    """Request model for event discovery"""
    city: str = Field(
        description="City name to search for events (e.g., 'Uppsala', 'Stockholm')"
    )
    max_events: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum number of events to discover"
    )


class EventStatusUpdateRequest(BaseModel):
    """Request model for updating event status"""
    status: Literal['pending', 'verified', 'archived'] = Field(
        description="New status for the event"
    )


class EventsListResponse(BaseModel):
    """Response for list of events"""
    events: List[StandaloneEvent]
    total: int
    limit: int
    offset: int


class EventDiscoveryResponse(BaseModel):
    """Response from event discovery"""
    run_id: str
    status: str
    city: str
    events_found: int
    events_saved: int
    started_at: str
    completed_at: str
