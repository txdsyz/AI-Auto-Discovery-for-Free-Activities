# 🎯 Complete Setup Guide - AfterClass Backend + Frontend

**Quick Start:** Backend API is ready! Frontend just needs to make HTTP requests.

---

## 📋 What's Complete

✅ **Backend (FastAPI)**
- Discovery service (finds orgs)
- Profiling service (extracts data)
- Firebase integration (saves data)
- API endpoints (serves data to frontend)
- CORS enabled (allows frontend requests)

✅ **Database (Firebase Firestore)**
- Organizations collection with discovery metadata
- Events collection linked to organizations
- Automatic duplicate checking

✅ **API Endpoints**
- `GET /organizations` - List all orgs with pagination
- `GET /organizations/{id}` - Get single org with events
- `POST /discover` - Run discovery pipeline

---

## 🚀 How to Run

### Step 1: Start Backend

```bash
cd backend
python main.py
```

Server runs on: `http://localhost:8000`
API docs: `http://localhost:8000/docs`

### Step 2: Test API (Optional)

```bash
# In another terminal
cd backend
python test_api.py
```

This will test all endpoints and show example responses.

### Step 3: Frontend Setup

**You DON'T need Firebase in frontend!** Just call the backend API.

```bash
cd frontend  # Your React/Next.js project

# Install dependencies
npm install

# Create .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start dev server
npm run dev
```

---

## 🔗 Frontend ↔ Backend Communication

### Architecture

```
Frontend (React/Next.js)
    ↓ HTTP requests (fetch/axios)
Backend (FastAPI)
    ↓ Firebase SDK
Database (Firestore)
```

**Key Point:** Frontend ONLY talks to backend via HTTP. No Firebase needed in frontend!

---

## 📡 API Examples for Frontend

### 1. List Organizations

```typescript
// Get all organizations with pagination
async function getOrganizations(page = 0, category?: string) {
  const limit = 10;
  const offset = page * limit;
  
  let url = `http://localhost:8000/organizations?limit=${limit}&offset=${offset}`;
  if (category) {
    url += `&category=${category}`;
  }
  
  const response = await fetch(url);
  const data = await response.json();
  
  return {
    organizations: data.organizations,
    total: data.total
  };
}
```

### 2. Get Single Organization

```typescript
async function getOrgDetails(orgId: string) {
  const response = await fetch(`http://localhost:8000/organizations/${orgId}`);
  return await response.json();
}
```

### 3. Run Discovery (Admin Feature)

```typescript
async function runDiscovery() {
  const response = await fetch('http://localhost:8000/discover', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      categories: ['sports', 'youth_centers'],
      max_organizations: 5
    })
  });
  
  return await response.json();
}
```

---

## 📂 Files You Need

### Backend (Already Complete ✅)

```
backend/
├── main.py                          # FastAPI app
├── app/
│   ├── api/
│   │   └── routes.py                # API endpoints ✅
│   ├── services/
│   │   ├── discovery.py             # Find orgs ✅
│   │   └── profiling.py             # Extract data ✅
│   └── integrations/
│       └── firebase.py              # Save to DB ✅
└── .env                             # API keys (don't commit!)
```

### Frontend (To Create)

```
frontend/
├── .env.local                       # Just API_URL
├── lib/
│   └── api.ts                       # API client (see guide)
├── app/
│   ├── organizations/
│   │   ├── page.tsx                 # List page
│   │   └── [id]/
│   │       └── page.tsx             # Detail page
│   └── admin/
│       └── page.tsx                 # Discovery trigger (optional)
```

**Copy the API client from:** `FRONTEND_BACKEND_GUIDE.md` (lines 204-275)

---

## 🎯 For Hackathon Demo

### Pre-populate Database

```bash
# Run this ONCE before demo to populate database
cd backend
python test_full_pipeline.py 1
```

This discovers 3-5 organizations and saves them to Firebase.

### During Demo

1. **Start backend:** `python main.py`
2. **Start frontend:** `npm run dev`
3. **Show organization list** - Instant load (data already in DB)
4. **Show organization details** - Instant load
5. **(Optional) Show discovery** - Button to find new orgs (takes 2-3 min)

**Pro tip:** Pre-populate database to avoid waiting during demo!

---

## 📊 Example API Responses

### GET /organizations

```json
{
  "organizations": [
    {
      "id": "abc123",
      "name": "Södermalms Volleybollklubb",
      "type": "Sports Club",
      "location": "Södermalm, Stockholm",
      "description": "Volleyball for youth ages 7-19",
      "contact": {
        "email": "info@example.se",
        "phone": "070-123 45 67"
      },
      "website": "https://example.se",
      "discovery": {
        "category": "sports",
        "search_query": "Södermalm idrottsförening ungdom"
      }
    }
  ],
  "total": 25,
  "limit": 10,
  "offset": 0
}
```

### GET /organizations/{id}

```json
{
  "id": "abc123",
  "name": "IF Söderkamraterna",
  "type": "Sports Club",
  "events": [
    {
      "id": "evt1",
      "name": "Training for F13",
      "type": "recurring",
      "schedule": "Måndagar 18-19",
      "age_range": "7-19"
    }
  ]
}
```

### POST /discover

```json
{
  "run_id": "run_xyz789",
  "status": "completed",
  "organizations_found": 5,
  "organizations_saved": 4,
  "irrelevant_filtered": 1
}
```

---

## 🛠️ Troubleshooting

### Backend won't start

```bash
# Check if port 8000 is in use
lsof -ti:8000 | xargs kill -9

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend can't connect

1. Check CORS: Backend allows `localhost:3000` ✅
2. Check URL: `NEXT_PUBLIC_API_URL=http://localhost:8000`
3. Check backend is running: Visit `http://localhost:8000/health`

### No organizations returned

```bash
# Populate database first
cd backend
python test_full_pipeline.py 1
```

---

## 📚 Documentation

- **Full Frontend Guide:** `FRONTEND_BACKEND_GUIDE.md`
- **API Documentation:** `http://localhost:8000/docs` (when server is running)
- **Backend Spec:** `docs/backend_spec.md`

---

## ✨ Summary

**Backend:** ✅ Complete and ready
**Frontend:** Just needs to make HTTP requests (see examples above)
**Database:** Firebase (handled by backend)
**Communication:** REST API (JSON over HTTP)

**No Firebase setup needed in frontend!** 🎉

---

## 🎬 Next Steps

1. **Start backend:** `python main.py`
2. **Test API:** `python test_api.py` (optional)
3. **Pre-populate DB:** `python test_full_pipeline.py 1`
4. **Build frontend:** Copy API client from guide
5. **Test end-to-end:** Frontend → Backend → Firebase

**You're ready for the hackathon!** 🚀
