# Events Backend - Quick Reference

## 🚀 Quick Start

### Test the Backend
```bash
# 1. Start backend server
cd backend
conda run -n afterclass uvicorn main:app --reload

# 2. In another terminal, test discovery
conda run -n afterclass python backend/test_event_discovery.py

# 3. Or test API endpoints
conda run -n afterclass python backend/test_events_api.py
```

### Discover Events Manually
```bash
curl -X POST http://localhost:8000/events/discover \
  -H "Content-Type: application/json" \
  -d '{"city": "Uppsala", "max_events": 5}'
```

### Get Events
```bash
# All events
curl http://localhost:8000/events

# Filter by city
curl "http://localhost:8000/events?city=Uppsala"

# Filter by status
curl "http://localhost:8000/events?status=pending"

# Multiple filters
curl "http://localhost:8000/events?city=Uppsala&status=pending&limit=20"
```

## 📁 Files Changed/Added

**Added:**
- `/backend/app/services/event_discovery.py` - Discovery service
- `/backend/test_event_discovery.py` - Discovery test
- `/backend/test_events_api.py` - API test
- `/docs/EVENTS_BACKEND.md` - Full documentation
- `/docs/EVENTS_IMPLEMENTATION_SUMMARY.md` - This summary

**Modified (additions only, no deletions):**
- `/backend/app/api/models.py` - Added event models
- `/backend/app/integrations/firebase.py` - Added event methods
- `/backend/app/api/routes.py` - Added event endpoints

**Unchanged:**
- All organization code
- All frontend code
- All existing tests

## 🗄️ Database

**New Collection:** `events`
- Completely separate from `organizations`
- Status: pending, verified, archived (3 states)
- Filterable by: city, status, sport_category, date

## 🔌 API Endpoints

| Method | Endpoint | Body |
|--------|----------|------|
| POST | `/events/discover` | `{"city": "Uppsala", "max_events": 10}` |
| GET | `/events` | Query params: city, status, sport_category, limit, offset |
| GET | `/events/{id}` | - |
| PATCH | `/events/{id}/status` | `{"status": "verified"}` |
| DELETE | `/events/{id}` | - |

## 🎯 Event Schema

```json
{
  "id": "abc123",
  "title": "Free Basketball Clinic",
  "sport_category": "basketball",
  "date": "2025-06-15",
  "time": "14:00",
  "location": "Fyrishov, Uppsala",
  "age_group": "10-16",
  "is_free": true,
  "summary": "Free basketball training...",
  "language": "sv",
  "source_url": "https://...",
  "city": "Uppsala",
  "status": "pending",
  "created_at": "2025-11-09T...",
  "last_updated": "2025-11-09T..."
}
```

## 🔍 Search Strategy

**Sports:** Basketball, Soccer, Swimming, Tennis, Volleyball, Handball, Hockey

**Languages:** English + Swedish queries

**Filters:** Only free activities for youth

**Extraction:** OpenAI → Regex fallback

## ✅ Status Workflow

- **pending** → Newly discovered
- **verified** → Confirmed legitimate
- **archived** → No longer active

## 📊 What's Working

✅ Event discovery service  
✅ Firebase CRUD operations  
✅ API endpoints  
✅ Status management  
✅ Filtering (city, status, sport, date)  
✅ Bilingual search  
✅ AI extraction with fallback  

## ⏳ What's Next

- Test with real cities
- Frontend integration (later)
- UI components for events tab

## 🛡️ Safety

✅ Zero breaking changes  
✅ Organizations untouched  
✅ Separate collection  
✅ Independent workflows  
✅ MVP remains stable  

---

**Full docs:** `/docs/EVENTS_BACKEND.md`
