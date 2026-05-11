# Frontend ↔ Backend Communication Guide

**Architecture:** Backend API with FastAPI → Frontend consumes JSON

---

## 🏗️ Architecture Overview

```
┌─────────────────┐
│  Frontend       │
│  (React/Next)   │
│                 │
│  - Display orgs │
│  - Filter/Search│
│  - Show events  │
└────────┬────────┘
         │ HTTP REST API
         │ (JSON)
         ↓
┌─────────────────┐
│  Backend        │
│  (FastAPI)      │
│                 │
│  - API Endpoints│
│  - Query Firebase│
│  - Run Scraping │
└────────┬────────┘
         │ Firebase SDK
         ↓
┌─────────────────┐
│  Firebase       │
│  Firestore DB   │
│                 │
│  - Organizations│
│  - Events       │
└─────────────────┘
```

---

## ✅ What's Already Done (Backend)

1. ✅ **Discovery Service** - Finds youth organizations
2. ✅ **Profiling Service** - Extracts contact info & events  
3. ✅ **Firebase Integration** - Saves to Firestore
4. ✅ **Discovery Metadata** - Tracks which category found each org
5. ✅ **API Endpoints** - Ready for frontend to consume

---

## 📡 API Endpoints for Frontend

### Base URL
```
http://localhost:8000
```

### 1. **Get All Organizations** (List Page)

**Endpoint:**
```
GET /organizations?limit=10&offset=0&category=sports
```

**Query Parameters:**
- `limit` (optional): Number of results (default: 10, max: 100)
- `offset` (optional): Pagination offset (default: 0)
- `category` (optional): Filter by category - `sports`, `youth_centers`, `scouts`, `cultural`

**Response:**
```json
{
  "organizations": [
    {
      "id": "abc123",
      "name": "Södermalms Volleybollklubb",
      "type": "Sports Club",
      "location": "Södermalm, Stockholm",
      "description": "Volleyball training for youth ages 7-19",
      "contact": {
        "email": "info@example.se",
        "phone": "070-123 45 67"
      },
      "website": "https://example.se",
      "discovery": {
        "category": "sports",
        "search_query": "Södermalm idrottsförening ungdom",
        "discovered_at": "2025-11-08T10:30:00Z"
      },
      "created_at": "2025-11-08T10:35:00Z",
      "last_updated": "2025-11-08T10:35:00Z"
    }
  ],
  "total": 25,
  "limit": 10,
  "offset": 0
}
```

**Frontend Example (JavaScript/TypeScript):**
```typescript
// Fetch organizations with pagination
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
    totalPages: Math.ceil(data.total / limit),
    currentPage: page
  };
}

// Usage in React component
const { organizations, totalPages } = await getOrganizations(0, 'sports');
```

---

### 2. **Get Single Organization** (Detail Page)

**Endpoint:**
```
GET /organizations/{org_id}
```

**Response:**
```json
{
  "id": "abc123",
  "name": "IF Söderkamraterna",
  "type": "Sports Club",
  "location": "Södermalm, Stockholm",
  "description": "Football club for youth ages 7-19",
  "contact": {
    "email": "info@soderkamraterna.se",
    "phone": "070-742 59 22"
  },
  "website": "https://soderkamraterna.se",
  "discovery": {
    "category": "sports",
    "search_query": "Södermalm fotbollsklubb barn"
  },
  "events": [
    {
      "id": "evt1",
      "organization_id": "abc123",
      "name": "Training for F13",
      "type": "recurring",
      "schedule": "Måndagar 18-19",
      "date": null,
      "age_range": "7-19",
      "description": "Weekly football training",
      "created_at": "2025-11-08T10:35:00Z"
    },
    {
      "id": "evt2",
      "organization_id": "abc123",
      "name": "Youth Tournament",
      "type": "one-time",
      "schedule": null,
      "date": "2025-12-15",
      "age_range": "10-15",
      "description": "Annual tournament"
    }
  ]
}
```

**Frontend Example:**
```typescript
async function getOrganizationDetails(orgId: string) {
  const response = await fetch(`http://localhost:8000/organizations/${orgId}`);
  
  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Organization not found');
    }
    throw new Error('Failed to fetch organization');
  }
  
  return await response.json();
}

// Usage in React component
const org = await getOrganizationDetails('abc123');
console.log(org.name, org.events);
```

---

### 3. **Run Discovery Pipeline** (Admin Feature)

**Endpoint:**
```
POST /discover
```

**Request Body:**
```json
{
  "categories": ["sports", "youth_centers"],
  "max_organizations": 5
}
```

**Response:**
```json
{
  "run_id": "run_xyz789",
  "status": "completed",
  "organizations_found": 5,
  "organizations_saved": 4,
  "irrelevant_filtered": 1,
  "started_at": "2025-11-08T10:00:00Z",
  "completed_at": "2025-11-08T10:05:00Z"
}
```

**Frontend Example:**
```typescript
async function runDiscovery(categories: string[], maxOrgs: number = 5) {
  const response = await fetch('http://localhost:8000/discover', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      categories: categories,
      max_organizations: maxOrgs
    })
  });
  
  return await response.json();
}

// Usage
const result = await runDiscovery(['sports', 'youth_centers'], 5);
console.log(`Found ${result.organizations_found} organizations`);
```

---

### 4. **Health Check**

**Endpoint:**
```
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-11-08T10:00:00Z"
}
```

---

## 🚀 Frontend Setup Steps

### 1. **No Firebase Setup Needed in Frontend!** ✅

You DON'T need to:
- Install Firebase SDK in frontend
- Manage Firebase keys in frontend
- Set up Firestore rules

Backend handles ALL Firebase operations.

### 2. **Environment Variables (Frontend)**

Create `.env.local` in your frontend:

```bash
# For development
NEXT_PUBLIC_API_URL=http://localhost:8000

# For production (deploy backend first)
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

### 3. **API Client (Recommended)**

Create `lib/api.ts`:

```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Organization {
  id: string;
  name: string;
  type: string;
  location: string;
  description: string;
  contact: {
    email: string | null;
    phone: string | null;
  };
  website: string;
  discovery: {
    category: string;
    search_query: string;
  };
  events?: Event[];
}

export interface Event {
  id: string;
  organization_id: string;
  name: string;
  type: 'recurring' | 'one-time';
  schedule: string | null;
  date: string | null;
  age_range: string | null;
  description: string;
}

class AfterClassAPI {
  async getOrganizations(params: {
    limit?: number;
    offset?: number;
    category?: string;
  } = {}) {
    const { limit = 10, offset = 0, category } = params;
    
    let url = `${API_URL}/organizations?limit=${limit}&offset=${offset}`;
    if (category) {
      url += `&category=${category}`;
    }
    
    const response = await fetch(url);
    if (!response.ok) throw new Error('Failed to fetch organizations');
    
    return response.json();
  }
  
  async getOrganization(id: string): Promise<Organization> {
    const response = await fetch(`${API_URL}/organizations/${id}`);
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Organization not found');
      }
      throw new Error('Failed to fetch organization');
    }
    
    return response.json();
  }
  
  async runDiscovery(categories: string[], maxOrgs: number = 5) {
    const response = await fetch(`${API_URL}/discover`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        categories,
        max_organizations: maxOrgs
      })
    });
    
    if (!response.ok) throw new Error('Discovery failed');
    return response.json();
  }
}

export const api = new AfterClassAPI();
```

### 4. **React Component Example**

```typescript
// app/organizations/page.tsx
'use client';

import { useEffect, useState } from 'react';
import { api, Organization } from '@/lib/api';

export default function OrganizationsPage() {
  const [orgs, setOrgs] = useState<Organization[]>([]);
  const [loading, setLoading] = useState(true);
  const [category, setCategory] = useState<string | undefined>();
  
  useEffect(() => {
    async function loadOrganizations() {
      try {
        setLoading(true);
        const data = await api.getOrganizations({ category });
        setOrgs(data.organizations);
      } catch (error) {
        console.error('Failed to load organizations:', error);
      } finally {
        setLoading(false);
      }
    }
    
    loadOrganizations();
  }, [category]);
  
  if (loading) return <div>Loading...</div>;
  
  return (
    <div>
      <h1>Youth Organizations in Stockholm</h1>
      
      {/* Category Filter */}
      <select onChange={(e) => setCategory(e.target.value || undefined)}>
        <option value="">All Categories</option>
        <option value="sports">Sports</option>
        <option value="youth_centers">Youth Centers</option>
        <option value="scouts">Scouts</option>
        <option value="cultural">Cultural</option>
      </select>
      
      {/* Organization List */}
      <div className="grid grid-cols-3 gap-4">
        {orgs.map(org => (
          <div key={org.id} className="card">
            <h2>{org.name}</h2>
            <p>{org.type} - {org.location}</p>
            <p>{org.description}</p>
            
            {/* Contact Info */}
            {org.contact.email && (
              <a href={`mailto:${org.contact.email}`}>
                {org.contact.email}
              </a>
            )}
            
            {/* Discovery Metadata */}
            <span className="badge">{org.discovery.category}</span>
            
            <a href={`/organizations/${org.id}`}>View Details →</a>
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## 🔧 Running Both Services

### Terminal 1: Backend
```bash
cd backend
python -m uvicorn app.main:app --reload
# Runs on http://localhost:8000
```

### Terminal 2: Frontend
```bash
cd frontend
npm run dev
# Runs on http://localhost:3000
```

---

## 🎯 Quick Start Checklist

### Backend (Already Done ✅)
- [x] Firebase integration working
- [x] API endpoints implemented
- [x] Discovery metadata tracked
- [x] CORS enabled for frontend

### Frontend (To Do)
- [ ] Install dependencies (no Firebase needed!)
- [ ] Create `.env.local` with API_URL
- [ ] Copy `lib/api.ts` client
- [ ] Build organization list page
- [ ] Build organization detail page
- [ ] (Optional) Add admin page for running discovery

---

## 💡 Pro Tips

1. **CORS Setup** (Already configured in backend)
   - Backend allows requests from localhost:3000
   - For production, add your frontend domain

2. **Error Handling**
   - Backend returns proper HTTP status codes
   - 404 = Not found
   - 500 = Server error
   - Handle these in frontend

3. **Loading States**
   - API calls can take 1-2 seconds
   - Always show loading indicators

4. **Caching** (Optional)
   - Use SWR or React Query for automatic caching
   - Reduces API calls

5. **Pagination**
   - Use limit/offset for large lists
   - 10-20 items per page is good

---

## 🚀 For Hackathon Demo

**Recommended Flow:**

1. **Pre-populate database:**
   ```bash
   cd backend
   python test_full_pipeline.py 1
   # This will discover and save 3-5 organizations
   ```

2. **Start backend:**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Frontend fetches data:**
   - No scraping during demo (too slow)
   - Just display pre-populated orgs
   - Instant page loads!

4. **Show discovery in admin panel:**
   - Button to trigger new discovery
   - Show progress/results

---

## 📊 Data Flow Example

```
User visits frontend
    ↓
Frontend: GET /organizations?category=sports
    ↓
Backend: Query Firebase Firestore
    ↓
Firebase: Return matching organizations
    ↓
Backend: Format as JSON + add metadata
    ↓
Frontend: Render organization cards
    ↓
User clicks organization
    ↓
Frontend: GET /organizations/{id}
    ↓
Backend: Get org + events from Firebase
    ↓
Frontend: Show details page with events
```

---

**TLDR:** Frontend only needs to call REST API endpoints. No Firebase setup required in frontend! Backend handles everything. 🎉
