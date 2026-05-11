# Backend Implementation TODO

**Project:** Youth Organization Discovery Pipeline  
**Focus:** Backend (FastAPI + Firebase + Tavily + OpenAI)  
**Target:** 3 organizations with 2-3 events each for demo  
**Estimated Time:** 5-6 hours

---

## Overview

This document tracks the implementation of a FastAPI backend that:
1. Discovers Swedish youth organizations in Stockholm via web search
2. Profiles organizations by extracting website content
3. Uses LLM to structure data (contact info, events, age ranges)
4. Stores everything in Firebase Firestore

**Frontend Note:** React + Tailwind frontend will be built separately after backend is complete.

---

## Phase 1: Project Setup (30 mins)

### 1.1 Create Project Structure
- [x] Create `backend/` directory
- [x] Set up the following structure:
  ```
  backend/
  ├── main.py
  ├── requirements.txt
  ├── .env.example
  ├── .gitignore
  ├── README.md
  ├── app/
  │   ├── __init__.py
  │   ├── config.py
  │   ├── api/
  │   │   ├── __init__.py
  │   │   ├── routes.py
  │   │   └── models.py
  │   ├── services/
  │   │   ├── __init__.py
  │   │   ├── discovery.py
  │   │   ├── profiling.py
  │   │   └── pipeline.py
  │   ├── integrations/
  │   │   ├── __init__.py
  │   │   ├── tavily.py
  │   │   ├── openai.py
  │   │   └── firebase.py
  │   └── utils/
  │       ├── __init__.py
  │       ├── prompts.py
  │       └── validators.py
  └── tests/
      ├── __init__.py
      ├── test_discovery.py
      └── test_profiling.py
  ```

### 1.2 Install Dependencies
- [x] Create Python virtual environment: `python -m venv venv` (use setup.sh)
- [x] Activate environment: `source venv/bin/activate`
- [x] Create `requirements.txt` with:
  ```txt
  fastapi==0.104.1
  uvicorn[standard]==0.24.0
  pydantic==2.5.0
  python-dotenv==1.0.0
  firebase-admin==6.3.0
  httpx==0.25.2
  openai==1.3.7
  tavily-python==0.3.0
  python-multipart==0.0.6
  ```
- [x] Install dependencies: `pip install -r requirements.txt` (use setup.sh)

### 1.3 Configure Environment Variables
- [x] Create `.env` file with:
  ```env
  TAVILY_API_KEY=tvly-your_key_here
  OPENAI_API_KEY=sk-your_key_here
  FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
  ```
- [ ] Create `.env.example` (without actual keys)
- [ ] Add `.env` to `.gitignore`

### 1.4 Set Up Firebase
- [ ] Go to [Firebase Console](https://console.firebase.google.com/)
- [ ] Create new project: "afterclass-discovery"
- [ ] Enable Firestore Database
- [ ] Generate service account credentials
- [ ] Download `firebase-credentials.json`
- [ ] Place in backend root (add to `.gitignore`)
- [ ] Create Firestore collections:
  - `organizations` (composite index: none needed initially)
  - `events` (composite index: `organization_id + created_at`)
  - `discovery_runs`

### 1.5 Initialize FastAPI App
- [ ] Create basic `main.py`:
  ```python
  from fastapi import FastAPI
  from fastapi.middleware.cors import CORSMiddleware
  
  app = FastAPI(title="Youth Organization Discovery API")
  
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],  # Update for production
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  
  @app.get("/")
  def root():
      return {"status": "ok", "message": "Youth Org Discovery API"}
  ```
- [ ] Test server: `uvicorn main:app --reload`
- [ ] Verify at `http://localhost:8000`

---

## Phase 2: API Integrations (1 hour) ✅ COMPLETE

### 2.1 Tavily Search Client (`app/integrations/tavily.py`)
- [x] Implement `TavilyClient` class
- [x] Add method: `async def search(query, max_results=5, search_depth="advanced")`
  - Base URL: `https://api.tavily.com/search`
  - Headers: `Authorization: Bearer {TAVILY_API_KEY}`
  - Body: `{ query, search_depth, max_results, include_domains: [".se"] }`
  - Return: List of `{url, title, content}` from response
- [x] Add error handling for HTTP status codes (400, 401, 429, 432, 433, 500)
- [x] Test with sample query: `"idrottsföreningar Stockholm ungdom"`

### 2.2 Tavily Crawl Client (same file) ✅ COMPLETE
- [x] Keep `extract()` method for backward compatibility
- [x] **ADD:** New `async def crawl(url, instructions, max_depth=2, max_breadth=10, limit=15, extract_depth="advanced")`
  - Endpoint: `POST https://api.tavily.com/crawl`
  - Body: `{ url, instructions, max_depth, max_breadth, limit, extract_depth, format: "markdown" }`
  - Return: `{ results: [{ url, raw_content }], failed_results: [] }`
  - **Why:** Crawls multiple pages (homepage, contact, events, about) vs single page
- [x] Handle failed URLs gracefully
- [x] 90-second timeout (crawling takes longer)
- [ ] Test with a real Swedish organization URL
- [x] **Note:** Crawl costs ~3 credits per org (vs 0.2 for extract) but gets much better data

### 2.3 OpenAI Client (`app/integrations/openai.py`) ✅ COMPLETE
- [x] Implement `OpenAIClient` class
- [x] **UPDATE:** Method signature to support `response_format` parameter
  - `async def completion(prompt, model="gpt-4o-mini", temperature=0.1, response_format=None)`
  - Use `openai.chat.completions.create()`
  - System message: "You are a data structuring assistant."
  - **Default model: gpt-4o-mini** (cost-effective, ~15x cheaper than gpt-4)
  - **NEW:** Add `response_format={"type": "json_object"}` for guaranteed JSON
  - Return parsed JSON response
- [x] Updated `parse_json_response()` to use JSON mode by default
- [x] Add retry logic for rate limits
- [x] Add JSON validation (ensure valid JSON response)
- [ ] Test with sample structuring prompt (not extraction - Tavily does that now)

### 2.4 Firebase Client (`app/integrations/firebase.py`) ✅ COMPLETE
- [x] Initialize Firebase Admin SDK
- [x] Implement `FirestoreClient` class
- [x] Add methods:
  - `async def add_organization(data: dict) -> str` (returns doc ID)
  - `async def add_event(data: dict) -> str`
  - `async def get_organization(org_id: str) -> dict`
  - `async def get_organization_by_url(url: str) -> dict` **← NEW: For deduplication**
  - `async def get_all_organizations(limit=10, offset=0) -> List[dict]`
  - `async def get_events_by_org(org_id: str) -> List[dict]`
  - `async def create_discovery_run(data: dict) -> str`
  - `async def update_discovery_run(run_id: str, data: dict)`
- [ ] Test each CRUD operation manually
- [ ] **Test deduplication:** Verify `get_organization_by_url` prevents re-processing

### 2.5 Integration Testing
- [ ] Test Tavily search returns valid Swedish org URLs
- [ ] **NEW:** Test Tavily crawl with instructions on a real Swedish org
  - Verify it crawls multiple pages (homepage, contact, events)
  - Check that instructions guide extraction properly
  - Confirm raw_content contains email/phone/events
- [ ] Test OpenAI can structure Swedish content to JSON
  - Use `response_format={"type": "json_object"}`
  - Verify guaranteed JSON output
- [ ] Test Firebase read/write operations
- [ ] Test deduplication: `get_organization_by_url` prevents re-crawling
- [ ] Document any API rate limits encountered (crawl uses more credits!)

---

## Phase 3: Core Pipeline (2 hours)

### 3.1 Stage 1: Organization Discovery (`app/services/discovery.py`)

#### Implement `discover_organizations(categories, max_orgs=3)`
- [ ] Create query mapping:
  ```python
  CATEGORY_QUERIES = {
      "sports": "idrottsföreningar Stockholm ungdom",
      "youth_centers": "fritidsgård Stockholm verksamhet",
      "scouts": "scoutkårer Stockholm",
      "cultural": "kulturföreningar Stockholm barn"
  }
  ```
- [ ] For each category:
  - [ ] Call `tavily.search(query, max_results=5, search_depth="advanced")`
  - [ ] Filter results for `.se` domains
  - [ ] Extract URLs
- [ ] Remove duplicate URLs
- [ ] Limit to `max_orgs`
- [ ] Return list of unique organization URLs
- [ ] Add logging for each step

#### Test Discovery
- [ ] Test with `["sports"]` - expect 3-5 Swedish org URLs
- [ ] Test with `["sports", "youth_centers"]` - expect more diverse results
- [ ] Verify all URLs are valid Swedish domains
- [ ] Log actual URLs found for inspection

### 3.2 Prompts (`app/utils/prompts.py`) ✅ COMPLETE

#### Create `CRAWL_INSTRUCTIONS` (NEW - for Tavily Crawl)
- [x] Write crawl instructions template:
  ```python
  CRAWL_INSTRUCTIONS = """
  Find and extract from this Swedish youth organization website:
  
  1. Organization Details:
     - Name and type (Sports Club, Youth Center, Scout Group, etc.)
     - Location in Stockholm (neighborhood or district)
     - Brief description of what they do
  
  2. Contact Information (CRITICAL):
     - Email address (check: contact page, footer, about page, headers)
     - Phone number if available
     - Look thoroughly across all pages
  
  3. Youth Events and Programs (ages 7-19):
     - Event/program names
     - Type: recurring or one-time
     - Schedule (for recurring: day and time, e.g., "Tuesdays 18:00-20:00")
     - Date (for one-time: YYYY-MM-DD format)
     - Age range (e.g., 8-14, 10-16)
     - Brief description
  
  Target: Find at least 2-3 events or programs for youth/teenagers (barn/ungdom).
  Focus on activities suitable for ages 7-19.
  """
  ```

#### Create `STRUCTURE_PROMPT` (REPLACES PROFILE_PROMPT)
- [x] Write simplified structuring prompt:
  ```python
  STRUCTURE_PROMPT = """
  Convert the following crawled content from a Swedish youth organization website into structured JSON.
  
  Crawled Content:
  {content}
  
  Return valid JSON in this exact format:
  {{
    "name": "Organization name",
    "type": "Organization type",
    "contact": {{
      "email": "email address or null",
      "phone": "phone number or null"
    }},
    "location": "Location in Stockholm",
    "description": "One sentence description",
    "events": [
      {{
        "name": "Event name",
        "type": "recurring or one-time",
        "schedule": "Schedule for recurring events",
        "date": "YYYY-MM-DD for one-time events",
        "age_range": "Target age range",
        "description": "Brief description"
      }}
    ]
  }}
  
  Rules:
  - Extract at least 2-3 events if available
  - Email is critical - extract if present
  - Age ranges should be 7-19 (youth/teenagers)
  - Use null for missing fields
  - Return ONLY valid JSON, no markdown or explanations
  """
  ```
  - [x] **Note:** Much simpler than old prompt - Tavily already extracted the data!### 3.3 Stage 2: Organization Profiling (`app/services/profiling.py`) ✅ COMPLETE REWRITE

#### Implement `profile_organization(url: str)` - NEW CRAWL-BASED APPROACH
- [x] **STEP 1:** Call `tavily.crawl()` with instructions
  - `url=url`
  - `instructions=CRAWL_INSTRUCTIONS` (from prompts.py)
  - `max_depth=2` (crawl 2 levels deep)
  - `max_breadth=10` (check up to 10 pages per level)
  - `limit=15` (total pages)
  - `extract_depth="advanced"`
- [x] **STEP 2:** Combine content from all crawled pages
  - Loop through `crawl_response['results']`
  - Concatenate all `raw_content` with page URLs as headers
  - Example: `"=== https://org.se/contact ===\n{content}"`
- [x] **STEP 3:** Truncate combined content to 15,000 chars (token limit)
- [x] **STEP 4:** Call `openai.completion()` with structuring prompt
  - Use `STRUCTURE_PROMPT.format(content=all_content)`
  - **CRITICAL:** Pass `response_format={"type": "json_object"}`
  - Model: `gpt-4o-mini`
- [x] **STEP 5:** Parse guaranteed JSON response
- [x] **STEP 6:** Validate required fields:
  - [x] `name` exists and non-empty
  - [x] `contact.email` OR `contact.phone` exists (at least one)
  - [x] Warn if no events (not fatal)
  - [x] Age ranges checked if events exist
- [x] If validation fails, raise `ValueError` with details
- [x] Add metadata: `website`, `created_at`, `last_updated`
- [x] Return complete organization profile dict

#### Error Handling
- [ ] Handle crawl failures (retry once with reduced depth)
- [ ] Handle invalid JSON from LLM (shouldn't happen with `response_format=json_object`)
- [ ] Handle missing contact info (log as critical error, skip org)
- [ ] Handle no events found (log warning, skip org)
- [ ] Add timeout handling (60 seconds max for crawling - slower than extract)

#### Test Profiling
- [ ] Test with known good URL (e.g., a major Stockholm sports club)
- [ ] **Verify crawl visits multiple pages** (check crawl_response['results'] length)
- [ ] Verify email extraction works (should be better with multi-page crawl)
- [ ] Verify events are extracted with proper structure
- [ ] Test error handling with bad URL
- [ ] **Test cost:** Monitor Tavily credits used (~3 per org)
- [ ] Log actual extracted data for quality check

### 3.4 Complete Pipeline Orchestration (`app/services/pipeline.py`)

#### Implement `run_discovery_pipeline(categories, max_orgs=3)`
- [ ] Create discovery run document in Firestore:
  ```python
  {
    "search_queries": [category_to_query(c) for c in categories],
    "status": "in_progress",
    "started_at": datetime.utcnow()
  }
  ```
- [ ] Get run_id from Firestore
- [ ] Call `discover_organizations(categories, max_orgs)`
- [ ] **DEDUPLICATION CHECK** - For each URL:
  - [ ] **Check Firebase first:** `existing_org = await firestore.get_organization_by_url(url)`
  - [ ] **If exists:** Skip profiling, fetch events, add to results (HUGE cost savings!)
  - [ ] **If new:** Proceed with profiling
  - [ ] Try to profile organization (use gpt-4o-mini)
  - [ ] If successful:
    - [ ] Save organization to Firestore
    - [ ] Save each event to Firestore (with `organization_id`)
    - [ ] Add to results list
  - [ ] If error:
    - [ ] Log error details
    - [ ] Continue to next URL
    - [ ] Track failed URLs
- [ ] Update discovery run status:
  ```python
  {
    "status": "completed",
    "organizations_found": len(successful),
    "total_events_extracted": total_events,
    "completed_at": datetime.utcnow(),
    "errors": failed_urls
  }
  ```
- [ ] Return complete results with run_id

#### Optimization (CRITICAL for Hackathon Cost Savings)
- [ ] **Implement Firebase deduplication check** (MUST HAVE - saves 80-90% costs)
  - Check `get_organization_by_url()` BEFORE calling `tavily.crawl()`
  - Crawl is expensive (~3 credits per org), so deduplication is critical!
- [ ] **Use gpt-4o-mini model** (15x cheaper than gpt-4)
- [ ] **Use `response_format=json_object`** (guaranteed valid JSON, no retry needed)
- [ ] Implement parallel profiling using `asyncio.gather()` (optional)
- [ ] Add progress tracking (current org / total orgs)
- [ ] Add execution time tracking
- [ ] Log when skipping existing organizations

#### Test Complete Pipeline
- [ ] Run with `["sports"]`, `max_orgs=2`
- [ ] Verify 2 organizations are saved to Firestore
- [ ] Verify events are linked correctly
- [ ] Check execution time (should be < 90 seconds)
- [ ] Inspect data quality in Firebase console

---

## Phase 4: API Endpoints (1 hour)

### 4.1 Pydantic Models (`app/api/models.py`)

#### Request Models
- [ ] `DiscoverRequest`:
  ```python
  class DiscoverRequest(BaseModel):
      categories: List[str]
      max_organizations: int = 3
  ```

#### Response Models
- [ ] `ContactInfo`:
  ```python
  class ContactInfo(BaseModel):
      email: Optional[str]
      phone: Optional[str]
  ```
- [ ] `Event`:
  ```python
  class Event(BaseModel):
      id: str
      name: str
      type: str  # "recurring" or "one-time"
      schedule: Optional[str]
      date: Optional[str]
      age_range: str
      description: str
  ```
- [ ] `Organization`:
  ```python
  class Organization(BaseModel):
      id: str
      name: str
      type: str
      website: str
      contact: ContactInfo
      location: str
      description: str
      events: List[Event] = []
  ```
- [ ] `DiscoverResponse`:
  ```python
  class DiscoverResponse(BaseModel):
      run_id: str
      status: str
      organizations: List[Organization]
      total_organizations: int
      total_events: int
      execution_time_seconds: float
      errors: List[dict] = []
  ```

### 4.2 API Routes (`app/api/routes.py`)

#### POST `/api/discover`
- [ ] Accept `DiscoverRequest` body
- [ ] Validate categories are valid
- [ ] Call `run_discovery_pipeline()`
- [ ] Track execution time
- [ ] Return `DiscoverResponse`
- [ ] Handle errors with proper HTTP status codes

#### GET `/api/organizations`
- [ ] Accept query params: `limit` (default 10), `offset` (default 0)
- [ ] Call `firestore.get_all_organizations(limit, offset)`
- [ ] For each org, fetch events
- [ ] Return paginated response:
  ```python
  {
    "organizations": [...],
    "total": count,
    "limit": limit,
    "offset": offset
  }
  ```

#### GET `/api/organizations/{org_id}`
- [ ] Validate org_id
- [ ] Call `firestore.get_organization(org_id)`
- [ ] Fetch associated events
- [ ] Return `Organization` model
- [ ] Return 404 if not found

#### GET `/api/discover/{run_id}` (Optional)
- [ ] Get discovery run status from Firestore
- [ ] Return status, progress, timestamps
- [ ] Useful for long-running operations

### 4.3 Wire Up Routes in `main.py`
- [ ] Import routes from `app.api.routes`
- [ ] Include router: `app.include_router(router, prefix="/api")`
- [ ] Test all endpoints in FastAPI docs at `/docs`

### 4.4 CORS Configuration
- [ ] Update CORS to allow frontend origin (for later)
- [ ] Set proper allowed methods and headers
- [ ] Consider environment-based CORS settings

---

## Phase 5: Testing & Quality Assurance (1 hour)

### 5.1 End-to-End Testing

#### Test Complete Discovery Flow
- [ ] Start server: `uvicorn main:app --reload`
- [ ] Call `POST /api/discover`:
  ```bash
  curl -X POST http://localhost:8000/api/discover \
    -H "Content-Type: application/json" \
    -d '{"categories": ["sports", "youth_centers"], "max_organizations": 3}'
  ```
- [ ] Verify response has 3 organizations
- [ ] Check each org has:
  - [ ] Valid name
  - [ ] Valid email (test if real)
  - [ ] 2-3 events
  - [ ] Proper age ranges (7-19)
  - [ ] Swedish location

#### Test Data Quality
- [ ] Open Firebase console
- [ ] Inspect `organizations` collection
- [ ] Manually verify 3 sample emails are real
- [ ] Check events have realistic schedules
- [ ] Verify age ranges make sense
- [ ] Check for duplicate organizations

#### Test API Endpoints
- [ ] Test `GET /api/organizations` - returns list
- [ ] Test `GET /api/organizations/{id}` - returns single org with events
- [ ] Test pagination works correctly
- [ ] Test 404 handling for invalid IDs

### 5.2 Error Scenario Testing

#### Test Edge Cases
- [ ] Test with invalid category name
- [ ] Test with `max_organizations=0`
- [ ] Test when Tavily returns no results
- [ ] Test when extraction fails (bad URL)
- [ ] Test when LLM returns invalid JSON
- [ ] Test when no email is found in content
- [ ] Test when no events are found
- [ ] Verify proper error messages returned

#### Test Rate Limits
- [ ] Monitor Tavily API usage
- [ ] Check OpenAI token consumption
- [ ] Verify retry logic works
- [ ] Document rate limit thresholds

### 5.3 Performance Testing

#### Measure Pipeline Performance
- [ ] Run discovery 3 times and average:
  - [ ] Stage 1 (Discovery) time
  - [ ] Stage 2 (Profiling per org) time
  - [ ] Total pipeline time
- [ ] Target: < 90 seconds for 3 orgs
- [ ] If too slow, implement parallel profiling

#### Optimize if Needed
- [ ] Enable parallel profiling with `asyncio.gather()`
- [ ] Reduce content truncation size if token limits hit
- [ ] Cache Tavily search results
- [ ] Use faster OpenAI model (gpt-3.5-turbo) if acceptable

### 5.4 Code Quality

#### Code Review Checklist
- [ ] All functions have type hints
- [ ] All functions have docstrings
- [ ] Error handling is comprehensive
- [ ] Logging is informative
- [ ] No hardcoded secrets
- [ ] Environment variables used properly
- [ ] Code follows PEP 8 style guide
- [ ] No unused imports

#### Documentation
- [ ] Update README.md with:
  - [ ] Setup instructions
  - [ ] Environment variables needed
  - [ ] How to run server
  - [ ] API endpoint documentation
  - [ ] Example requests/responses
- [ ] Add inline comments for complex logic
- [ ] Document any known limitations

---

## Phase 6: Demo Preparation (30 mins)

### 6.1 Generate Demo Data
- [ ] Create `scripts/generate_demo_data.py`
- [ ] Run pipeline to generate 3 real organizations
- [ ] Export to `demo-data.json`:
  ```bash
  python scripts/generate_demo_data.py > demo-data.json
  ```
- [ ] Manually review data quality:
  - [ ] Contact emails are valid
  - [ ] Events are realistic
  - [ ] Age ranges appropriate
  - [ ] Descriptions are clear

### 6.2 Document Results
- [ ] Create `RESULTS.md` with:
  - [ ] Actual organizations discovered
  - [ ] Contact info found
  - [ ] Events extracted
  - [ ] Any data quality issues
  - [ ] Execution time metrics
  - [ ] API usage statistics

### 6.3 Prepare for Frontend
- [ ] Document API endpoints for frontend team
- [ ] Export OpenAPI schema: `GET /openapi.json`
- [ ] Create sample frontend API calls
- [ ] Ensure CORS is configured for local frontend dev
- [ ] Consider deploying backend (optional):
  - [ ] Railway, Render, or Google Cloud Run
  - [ ] Set up environment variables in platform
  - [ ] Test deployed API

---

## Success Criteria

✅ **Backend is complete when:**

- [ ] Pipeline discovers 3 organizations consistently
- [ ] Each organization has:
  - [ ] Valid name and website
  - [ ] Real email address (verified manually)
  - [ ] 2-3 events with proper structure
  - [ ] Age ranges between 7-19
  - [ ] Swedish location in Stockholm
- [ ] All API endpoints work correctly
- [ ] Data is persisted in Firebase
- [ ] Execution time < 90 seconds
- [ ] Error handling prevents crashes
- [ ] Code is well-documented
- [ ] Demo data is ready for frontend

---

## Known Challenges & Solutions

### Challenge 0: API Cost Management (NEW - CRITICAL for Hackathon)
**Problem:** Re-running pipeline wastes API credits (crawl is expensive!)  
**Solution:**
- ✅ **Check Firebase before profiling** (prevents re-processing same orgs)
  - **CRITICAL with crawl:** ~3 credits per org vs 0.2 for extract
  - Deduplication saves 80-90% of costs during testing
- ✅ **Use gpt-4o-mini** (15x cheaper than gpt-4, still excellent quality)
- ✅ **Use Tavily crawl with instructions** (better data quality, worth the cost)
- ✅ **Log skipped organizations** (see savings in action)
- **Result:** ~85-90% cost reduction during development/testing

### Challenge 1: Email Extraction Accuracy
**Problem:** LLM might miss contact emails  
**Solution:**
- Emphasize in prompt that email is CRITICAL
- Add validation that fails without email
- Consider extracting contact page separately
- Fallback: Use Tavily search for "[org name] Stockholm contact"

### Challenge 2: Swedish Content Parsing
**Problem:** LLM might struggle with Swedish text  
**Solution:**
- Use gpt-4o-mini (excellent multilingual support, cost-effective)
- **Tavily crawl already extracts clean Swedish text** (LLM just structures it)
- Use `response_format=json_object` for guaranteed valid JSON
- Include Swedish examples in prompt
- Test with multiple Swedish org types

### Challenge 3: Event Date Parsing
**Problem:** Swedish date formats, recurring vs one-time  
**Solution:**
- Provide clear format instructions in prompt
- Use examples in prompt (e.g., "Tisdagar 18:00-20:00")
- Validate date formats in code
- Default to recurring if unclear

### Challenge 4: Rate Limits
**Problem:** API limits on Tavily/OpenAI  
**Solution:**
- Tavily: 100 requests/month free (monitor usage)
- OpenAI: gpt-4o-mini has high rate limits
- **Firebase deduplication reduces API calls by 80-90%**
- Use rate limiting and retry logic
- Consider upgrading plans if needed

### Challenge 5: Execution Time
**Problem:** Sequential profiling is slow (especially with crawling)  
**Solution:**
- **Firebase checks are instant** (skip already-processed orgs)
- **Crawling takes ~25-35 seconds per org** (vs 15-20 for extract)
- Implement parallel profiling with `asyncio.gather()`
- Set reasonable timeouts (60s per org for crawling)
- Skip orgs that timeout
- gpt-4o-mini is faster than gpt-4
- **Worth the time:** Better data quality (multi-page coverage)

---

## Next Steps After Backend Complete

1. **Frontend Development** (separate sprint)
   - React app with Tailwind CSS
   - Use demo data initially
   - Connect to backend API
   - Display organizations in cards
   - Filter by category, age range
   - Show event schedules

2. **Backend Enhancements** (future)
   - Add more categories (music, arts, etc.)
   - Implement organization search
   - Add favorites/bookmarking
   - Email validation API integration
   - Auto-refresh stale data
   - Admin dashboard

3. **Production Deployment** (optional)
   - Deploy backend to cloud
   - Set up monitoring/logging
   - Configure production CORS
   - Set up CI/CD pipeline
   - Add API authentication

---

## Notes

- **Focus:** Backend only for now, frontend comes later
- **Quality over quantity:** 3 high-quality orgs better than 10 poor ones
- **Email is critical:** Pipeline should fail if no email found
- **Test with real data:** Don't mock - use actual Swedish organizations
- **Time budget:** 5-6 hours total, adjust if needed
- **Documentation:** Keep this TODO updated as you progress

---

## Progress Tracking

**Current Phase:** Phase 2 - API Integrations (In Progress)  
**Completed Tasks:** ~25 / ~100  
**Blockers:** None  
**Next Action:** 
1. Update `tavily.py` to add `crawl()` method (remove old `extract()` if exists)
2. Update `openai.py` to support `response_format` parameter
3. Update `prompts.py` with new `CRAWL_INSTRUCTIONS` and `STRUCTURE_PROMPT`
4. Rewrite `profiling.py` to use crawl-based approach
5. Test complete pipeline with new architecture

---

**Last Updated:** 8 November 2025  
**Status:** Ready to begin implementation
