# Events Backend Implementation

## Overview
Standalone events collection for discovering and managing free youth sports activities. This is completely separate from the organizations collection to maintain MVP stability.

## Database Schema

### Collection: `events`

```javascript
{
  id: string,
  title: string,
  sport_category: string,  // basketball, soccer, swimming, tennis, volleyball, handball, hockey, multiple, other
  date: string | null,     // YYYY-MM-DD format
  time: string | null,     // HH:MM format
  location: string,
  age_group: string,       // "6-12", "13-18", "all youth", etc.
  is_free: boolean,        // always true
  summary: string,         // English description
  language: string,        // "en" or "sv"
  source_url: string,
  city: string,
  status: string,          // "pending", "verified", "archived"
  created_at: timestamp,
  last_updated: timestamp
}
```

## API Endpoints

### 1. Discover Events
**POST** `/events/discover`

Discovers free youth sports events for a specific city using web search and AI extraction.

**Request:**
```json
{
  "city": "Uppsala",
  "max_events": 10
}
```

**Response:**
```json
{
  "run_id": "event_discovery_uppsala_20251109_143022",
  "status": "completed",
  "city": "Uppsala",
  "events_found": 8,
  "events_saved": 8,
  "started_at": "2025-11-09T14:30:22.123456",
  "completed_at": "2025-11-09T14:31:45.654321"
}
```

### 2. List Events
**GET** `/events`

Get list of events with optional filtering.

**Query Parameters:**
- `city` (optional): Filter by city name
- `status` (optional): pending, verified, or archived
- `sport_category` (optional): basketball, soccer, etc.
- `date_from` (optional): YYYY-MM-DD
- `date_to` (optional): YYYY-MM-DD
- `limit` (default: 100): Max results
- `offset` (default: 0): Pagination offset

**Example:**
```bash
GET /events?city=Uppsala&status=pending&limit=20
```

**Response:**
```json
{
  "events": [
    {
      "id": "abc123",
      "title": "Free Basketball Clinic",
      "sport_category": "basketball",
      "date": "2025-06-15",
      "time": "14:00",
      "location": "Fyrishov, Uppsala",
      "age_group": "10-16",
      "is_free": true,
      "summary": "Free basketball training for youth...",
      "language": "sv",
      "source_url": "https://example.com/event",
      "city": "Uppsala",
      "status": "pending",
      "created_at": "2025-11-09T14:30:00.000000",
      "last_updated": "2025-11-09T14:30:00.000000"
    }
  ],
  "total": 1,
  "limit": 20,
  "offset": 0
}
```

### 3. Get Single Event
**GET** `/events/{event_id}`

Get details for a specific event.

**Response:** Single event object

### 4. Update Event Status
**PATCH** `/events/{event_id}/status`

Update the status of an event.

**Request:**
```json
{
  "status": "verified"
}
```

**Response:**
```json
{
  "success": true,
  "event_id": "abc123",
  "new_status": "verified",
  "message": "Event status updated to verified"
}
```

### 5. Delete Event
**DELETE** `/events/{event_id}`

Delete an event from the database.

**Response:**
```json
{
  "success": true,
  "event_id": "abc123",
  "message": "Event deleted successfully"
}
```

## Backend Components

### 1. Models (`app/api/models.py`)
- `StandaloneEvent`: Event data model
- `EventDiscoveryRequest`: Discovery request validation
- `EventStatusUpdateRequest`: Status update validation
- `EventsListResponse`: List response format
- `EventDiscoveryResponse`: Discovery result format

### 2. Firebase Integration (`app/integrations/firebase.py`)
- `save_event()`: Save event to Firestore
- `get_events()`: Query events with filters
- `get_event_by_id()`: Get single event
- `update_event_status()`: Update event status
- `delete_event()`: Delete event
- `get_events_count()`: Count events with filters

### 3. Event Discovery Service (`app/services/event_discovery.py`)
- `discover_events_for_city()`: Main discovery orchestration
- `generate_event_search_queries()`: Create search queries (English + Swedish)
- `extract_event_from_text()`: AI-powered extraction using OpenAI
- `fallback_event_extraction()`: Regex-based fallback

### 4. API Routes (`app/api/routes.py`)
- Event endpoints starting at line ~285
- All routes prefixed with `/events`

## Search Strategy

### Search Queries
Generates bilingual queries combining:
- **English templates:** "free youth basketball activities {city}", "free kids soccer program {city}"
- **Swedish templates:** "gratis ungdomsaktiviteter sport {city}", "gratis barn fotboll {city}"
- **Sports covered:** Basketball, Soccer, Swimming, Tennis, Volleyball, Handball, Hockey

### Extraction Pipeline
1. Search using Tavily (3 results per query)
2. Extract raw content from each webpage
3. Filter: Must contain "gratis", "free", or "kostnadsfri"
4. AI extraction with OpenAI (structured JSON)
5. Fallback to regex extraction if AI fails
6. Save to Firestore with "pending" status

## Testing

### Test Discovery Service
```bash
cd backend
conda run -n afterclass python test_event_discovery.py
```

This will:
- Run event discovery for Uppsala
- Save events to Firestore
- Test retrieval and filtering
- Display results

### Test API Endpoints
Make sure backend is running, then:
```bash
conda run -n afterclass python test_events_api.py
```

This will test:
- Event discovery endpoint
- GET events with filters
- GET single event
- PATCH status update
- Filter by city and status

### Manual API Testing
```bash
# 1. Start backend
cd backend
conda run -n afterclass uvicorn main:app --reload

# 2. Discover events
curl -X POST http://localhost:8000/events/discover \
  -H "Content-Type: application/json" \
  -d '{"city": "Uppsala", "max_events": 5}'

# 3. Get all events
curl http://localhost:8000/events?limit=10

# 4. Filter by city
curl http://localhost:8000/events?city=Uppsala

# 5. Update status
curl -X PATCH http://localhost:8000/events/{event_id}/status \
  -H "Content-Type: application/json" \
  -d '{"status": "verified"}'
```

## Status Workflow

Events have a simpler 3-state workflow:
- **pending**: Newly discovered, awaiting verification
- **verified**: Confirmed as legitimate and relevant
- **archived**: No longer active or relevant

## Frontend Integration (Not Yet Implemented)

When ready to connect frontend:

### TypeScript Types
```typescript
export interface StandaloneEvent {
  id: string;
  title: string;
  sport_category: string;
  date: string | null;
  time: string | null;
  location: string;
  age_group: string;
  is_free: boolean;
  summary: string;
  language: 'en' | 'sv';
  source_url: string;
  city: string;
  status: 'pending' | 'verified' | 'archived';
  created_at: string;
  last_updated: string;
}
```

### API Client Methods
```typescript
// In frontend/src/lib/api.ts
export const api = {
  // ... existing methods ...
  
  // Events
  discoverEvents: async (city: string, maxEvents: number) => {
    const response = await fetch(`${BASE_URL}/events/discover`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ city, max_events: maxEvents })
    });
    return response.json();
  },
  
  getEvents: async (filters?: {
    city?: string;
    status?: string;
    sport_category?: string;
    limit?: number;
  }) => {
    const params = new URLSearchParams();
    if (filters?.city) params.append('city', filters.city);
    if (filters?.status) params.append('status', filters.status);
    if (filters?.sport_category) params.append('sport_category', filters.sport_category);
    if (filters?.limit) params.append('limit', filters.limit.toString());
    
    const response = await fetch(`${BASE_URL}/events?${params}`);
    return response.json();
  },
  
  updateEventStatus: async (eventId: string, status: string) => {
    const response = await fetch(`${BASE_URL}/events/${eventId}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status })
    });
    return response.json();
  }
};
```

## Key Differences from Organizations

| Feature | Organizations | Events |
|---------|--------------|--------|
| Collection | `organizations` | `events` |
| Discovery | Org websites via Tavily crawl | Event searches via Tavily |
| Embedded Data | Has events array | Standalone (no nested data) |
| Status States | 4 (pending, check, onboarded, archived) | 3 (pending, verified, archived) |
| Data Source | Organization websites | Event listings, city pages |
| Frontend Tab | Organizations tab | Events tab (separate) |

## No Breaking Changes

✅ Organizations collection untouched  
✅ Existing routes unchanged  
✅ Separate Firestore collection  
✅ Independent discovery flow  
✅ Can be developed/tested separately  
✅ MVP remains stable  

## Next Steps

1. ✅ Backend implementation complete
2. ⏳ Test discovery with real cities
3. ⏳ Frontend UI components (when ready)
4. ⏳ Connect Events tab to API
5. ⏳ Add event details view
6. ⏳ Implement status management UI
