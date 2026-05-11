# Youth Organization Discovery Pipeline - Backend Specification

## Project Overview

A FastAPI backend that discovers youth organizations in Stockholm, profiles them, and extracts their events/programs. The system uses a two-stage pipeline: (1) Organization Discovery via web search, (2) Deep profiling via content extraction and LLM analysis.

**Target Output:** 3 organizations with 2-3 events each for hackathon demo.

---

## Tech Stack

- **Backend Framework:** FastAPI
- **Database:** Firebase Firestore
- **Search API:** Tavily Search API (`/search`)
- **Crawling & Extraction:** Tavily Crawl API (`/crawl`) with instructions
- **LLM:** OpenAI GPT-4o-mini (for JSON structuring only)
- **Language:** Python 3.10+
- **Cost Optimization:** Deduplication via Firebase checks + guided crawling

---

## Environment Variables

Create `.env` file:

```env
TAVILY_API_KEY=your_tavily_key
OPENAI_API_KEY=your_openai_key
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
```

---

## Database Schema (Firestore)

### Collection: `organizations`

```json
{
  "id": "auto_generated_id",
  "name": "Rinkeby IF",
  "type": "Sports Club",
  "website": "https://rinkebyif.se",
  "contact": {
    "email": "info@rinkebyif.se",
    "phone": "+46 8 XXX XXXX"
  },
  "location": "Rinkeby, Stockholm",
  "description": "Sports club offering football and basketball for youth",
  "created_at": "2025-11-08T10:30:00Z",
  "last_updated": "2025-11-08T10:30:00Z"
}
```

### Collection: `events`

```json
{
  "id": "auto_generated_id",
  "organization_id": "org_doc_id",
  "name": "Football Training",
  "type": "recurring",
  "schedule": "Mondays & Wednesdays 17:00-19:00",
  "date": null,
  "age_range": "8-14",
  "description": "Weekly football training sessions",
  "created_at": "2025-11-08T10:30:00Z"
}
```

### Collection: `discovery_runs`

Track each discovery pipeline execution:

```json
{
  "id": "auto_generated_id",
  "search_queries": [
    "idrottsföreningar Stockholm ungdom",
    "fritidsgård Stockholm verksamhet"
  ],
  "organizations_found": 3,
  "total_events_extracted": 7,
  "status": "completed",
  "started_at": "2025-11-08T10:25:00Z",
  "completed_at": "2025-11-08T10:30:00Z",
  "error": null
}
```

---

## API Endpoints

### 1. Run Discovery Pipeline

**POST** `/api/discover`

Executes the full two-stage pipeline.

**Request Body:**
```json
{
  "categories": ["sports", "youth_centers"],
  "max_organizations": 3
}
```

**Response:**
```json
{
  "run_id": "run_xyz123",
  "status": "completed",
  "organizations": [
    {
      "id": "org_123",
      "name": "Rinkeby IF",
      "type": "Sports Club",
      "website": "https://rinkebyif.se",
      "contact": {
        "email": "info@rinkebyif.se",
        "phone": "+46 8 XXX XXXX"
      },
      "location": "Rinkeby, Stockholm",
      "description": "Sports club offering football and basketball",
      "events": [
        {
          "id": "event_456",
          "name": "Football Training",
          "type": "recurring",
          "schedule": "Mon & Wed 17:00-19:00",
          "age_range": "8-14",
          "description": "Weekly training sessions"
        }
      ]
    }
  ],
  "total_organizations": 3,
  "total_events": 7,
  "execution_time_seconds": 45.2
}
```

### 2. Get All Organizations

**GET** `/api/organizations`

Returns all discovered organizations.

**Query Parameters:**
- `limit`: int (default: 10)
- `offset`: int (default: 0)

**Response:**
```json
{
  "organizations": [...],
  "total": 15,
  "limit": 10,
  "offset": 0
}
```

### 3. Get Organization by ID

**GET** `/api/organizations/{org_id}`

Returns single organization with all its events.

**Response:**
```json
{
  "id": "org_123",
  "name": "Rinkeby IF",
  "type": "Sports Club",
  "website": "https://rinkebyif.se",
  "contact": {...},
  "location": "Rinkeby, Stockholm",
  "description": "...",
  "events": [...]
}
```

### 4. Get Discovery Run Status

**GET** `/api/discover/{run_id}`

Check status of a discovery pipeline run.

**Response:**
```json
{
  "run_id": "run_xyz123",
  "status": "in_progress",
  "progress": {
    "stage": "profiling",
    "current_org": 2,
    "total_orgs": 3
  },
  "started_at": "2025-11-08T10:25:00Z"
}
```

---

## Pipeline Implementation

### Stage 1: Organization Discovery

**Function:** `discover_organizations()`

**Input:** Search categories
**Output:** List of organization URLs

**Logic:**
1. Map category to Swedish search query:
   - `sports` → "idrottsföreningar Stockholm ungdom"
   - `youth_centers` → "fritidsgård Stockholm verksamhet"
   
2. Execute Tavily search for each query:
   ```python
   tavily.search(
       query=search_query,
       search_depth="advanced",
       max_results=5,
       include_domains=[".se"]
   )
   ```

3. Extract organization URLs from search results:
   - Parse title and URL
   - Filter for Swedish domains (.se)
   - Remove duplicates
   - Limit to `max_organizations`

4. Return list of unique organization URLs

**Pseudo-code:**
```python
async def discover_organizations(categories: List[str], max_orgs: int = 3):
    query_map = {
        "sports": "idrottsföreningar Stockholm ungdom",
        "youth_centers": "fritidsgård Stockholm verksamhet"
    }
    
    all_urls = []
    
    for category in categories:
        query = query_map[category]
        results = await tavily_search(query, max_results=5)
        
        for result in results:
            url = result['url']
            if '.se' in url and url not in all_urls:
                all_urls.append(url)
    
    return all_urls[:max_orgs]
```

---

### Stage 2: Organization Profiling

**Function:** `profile_organization(url: str)`

**Input:** Organization website URL
**Output:** Organization data + events

**Logic:**
1. **Crawl organization website using Tavily Crawl with guided instructions:**
   ```python
   crawl_response = tavily.crawl(
       url=org_url,
       instructions="""
       Find and extract:
       - Organization name and type
       - Contact information (email, phone) - check contact page, footer, about page
       - Location in Stockholm
       - Description of organization
       - All events or programs for youth ages 7-19
       - For each event: name, schedule/date, age range, description
       """,
       max_depth=2,        # Crawl 2 levels deep (homepage + linked pages)
       max_breadth=10,     # Check up to 10 pages per level
       limit=15,           # Total pages to process
       extract_depth="advanced",
       format="markdown"
   )
   ```
   
   **Why Crawl instead of Extract:**
   - Crawls multiple pages (homepage, contact page, events page, about)
   - Instructions guide Tavily to focus on relevant data
   - Better coverage of contact info and events
   - Cleaner content extraction

2. **Combine crawled content from multiple pages:**
   ```python
   all_content = ""
   for page in crawl_response['results']:
       all_content += f"\n\n=== {page['url']} ===\n{page['raw_content']}"
   ```

3. **Use OpenAI to structure the crawled data into JSON:**
   - OpenAI receives pre-cleaned content from Tavily
   - Simplified prompt: just structure data, not extract
   - More reliable than pure extraction
   - Uses `response_format={"type": "json_object"}` for guaranteed JSON

4. **Validate required fields:**
   - name (required)
   - email or phone (at least one required)
   - events array (minimum 1 event)

5. **Return structured organization profile**

**Tavily Crawl Instructions:**
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

**OpenAI Structuring Prompt (Simplified):**
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

**Pseudo-code:**
```python
async def profile_organization(url: str):
    # STEP 1: Crawl organization website with instructions
    crawl_response = await tavily_crawl(
        url=url,
        instructions=CRAWL_INSTRUCTIONS,
        max_depth=2,
        max_breadth=10,
        limit=15,
        extract_depth="advanced"
    )
    
    # STEP 2: Combine content from all crawled pages
    all_content = ""
    for page in crawl_response.get('results', []):
        page_url = page.get('url', '')
        page_content = page.get('raw_content', '')
        all_content += f"\n\n=== {page_url} ===\n{page_content}"
    
    # Truncate if too long (stay under token limits)
    if len(all_content) > 15000:
        all_content = all_content[:15000]
    
    # STEP 3: Use OpenAI to structure the crawled data
    prompt = STRUCTURE_PROMPT.format(content=all_content)
    response = await openai_completion(
        prompt=prompt,
        model="gpt-4o-mini",
        response_format={"type": "json_object"}  # Force JSON response
    )
    
    # STEP 4: Parse JSON
    profile = json.loads(response)
    
    # STEP 5: Validate
    if not profile.get('name'):
        raise ValueError("Missing organization name")
    if not profile.get('contact', {}).get('email') and not profile.get('contact', {}).get('phone'):
        raise ValueError("Missing contact information")
    
    # STEP 6: Add metadata
    profile['website'] = url
    profile['created_at'] = datetime.utcnow()
    
    return profile
```

---

### Complete Pipeline Flow

**Function:** `run_discovery_pipeline()`

```python
async def run_discovery_pipeline(categories: List[str], max_orgs: int = 3):
    # Create discovery run document
    run_doc = {
        "search_queries": [category_to_query(c) for c in categories],
        "status": "in_progress",
        "started_at": datetime.utcnow()
    }
    run_id = firestore.collection('discovery_runs').add(run_doc)
    
    try:
        # STAGE 1: Discover organizations
        org_urls = await discover_organizations(categories, max_orgs)
        
        # STAGE 2: Profile each organization
        organizations = []
        
        for url in org_urls:
            try:
                # OPTIMIZATION: Check if org already exists in database
                existing_org = await firestore.get_organization_by_url(url)
                if existing_org:
                    print(f"⚡ Skipping {url} - already in database")
                    # Fetch events for existing org
                    events = await firestore.get_events_by_org(existing_org['id'])
                    existing_org['events'] = events
                    organizations.append(existing_org)
                    continue
                
                # Profile new organization
                profile = await profile_organization(url)
                
                # Save to Firestore
                org_ref = firestore.collection('organizations').add({
                    "name": profile['name'],
                    "type": profile['type'],
                    "website": profile['website'],
                    "contact": profile['contact'],
                    "location": profile['location'],
                    "description": profile['description'],
                    "created_at": profile['created_at']
                })
                
                # Save events
                for event in profile['events']:
                    firestore.collection('events').add({
                        "organization_id": org_ref.id,
                        **event,
                        "created_at": datetime.utcnow()
                    })
                
                # Add to response
                profile['id'] = org_ref.id
                organizations.append(profile)
                
            except Exception as e:
                print(f"Error profiling {url}: {e}")
                continue
        
        # Update discovery run
        firestore.collection('discovery_runs').document(run_id).update({
            "status": "completed",
            "organizations_found": len(organizations),
            "total_events_extracted": sum(len(o['events']) for o in organizations),
            "completed_at": datetime.utcnow()
        })
        
        return {
            "run_id": run_id,
            "status": "completed",
            "organizations": organizations
        }
        
    except Exception as e:
        # Update run as failed
        firestore.collection('discovery_runs').document(run_id).update({
            "status": "failed",
            "error": str(e),
            "completed_at": datetime.utcnow()
        })
        raise
```

---

## Project Structure

```
backend/
├── main.py                  # FastAPI app entry point
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (gitignored)
├── firebase-credentials.json # Firebase admin SDK (gitignored)
│
├── app/
│   ├── __init__.py
│   ├── config.py           # Load env vars, configs
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py       # API endpoint handlers
│   │   └── models.py       # Pydantic request/response models
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── discovery.py    # Stage 1: Organization discovery
│   │   ├── profiling.py    # Stage 2: Organization profiling
│   │   └── pipeline.py     # Complete pipeline orchestration
│   │
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── tavily.py       # Tavily API client
│   │   ├── openai.py       # OpenAI API client
│   │   └── firebase.py     # Firebase Firestore client
│   │
│   └── utils/
│       ├── __init__.py
│       ├── prompts.py      # LLM prompt templates
│       └── validators.py   # Data validation helpers
│
└── tests/
    ├── __init__.py
    ├── test_discovery.py
    └── test_profiling.py
```

---

## Requirements.txt

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

---

## Implementation Order

### Phase 1: Setup (30 mins)
1. Create project structure
2. Install dependencies
3. Set up Firebase project
4. Configure environment variables
5. Initialize FastAPI app

### Phase 2: Integrations (1 hour)
1. Implement Tavily search client (`/search` endpoint)
2. Implement Tavily crawl client (`/crawl` endpoint with instructions)
3. Implement OpenAI client (use gpt-4o-mini with `response_format=json_object`)
4. Implement Firebase Firestore client (add get_organization_by_url method)
5. Test each integration independently

### Phase 3: Core Pipeline (2 hours)
1. Implement Stage 1: `discover_organizations()`
2. Test with real search queries
3. Implement Stage 2: `profile_organization()` (use gpt-4o-mini)
4. Test with sample organization URLs
5. Implement complete pipeline orchestration with Firebase deduplication
6. Add error handling and retries

### Phase 4: API Endpoints (1 hour)
1. Create Pydantic models for requests/responses
2. Implement `/api/discover` endpoint
3. Implement `/api/organizations` endpoint
4. Implement `/api/organizations/{id}` endpoint
5. Add CORS middleware for frontend

### Phase 5: Testing (1 hour)
1. Test complete pipeline end-to-end
2. Verify data quality (contact info extraction)
3. Test error scenarios
4. Optimize LLM prompts if needed
5. Document actual results in README

---

## Testing Strategy

### Unit Tests

Test each function independently:

```python
# Test Stage 1
async def test_discover_organizations():
    urls = await discover_organizations(["sports"], max_orgs=3)
    assert len(urls) <= 3
    assert all('.se' in url for url in urls)

# Test Stage 2
async def test_profile_organization():
    profile = await profile_organization("https://example-org.se")
    assert profile['name']
    assert profile['contact']['email']
    assert len(profile['events']) >= 1
```

### Integration Test

Test complete pipeline:

```python
async def test_complete_pipeline():
    result = await run_discovery_pipeline(["sports"], max_orgs=2)
    
    assert result['status'] == 'completed'
    assert len(result['organizations']) == 2
    
    for org in result['organizations']:
        assert org['name']
        assert org['contact']['email']
        assert len(org['events']) >= 2
```

### Manual Testing

Run pipeline and inspect results:

```bash
# Start server
uvicorn main:app --reload

# Call API
curl -X POST http://localhost:8000/api/discover \
  -H "Content-Type: application/json" \
  -d '{"categories": ["sports", "youth_centers"], "max_organizations": 3}'

# Check results in Firebase console
# Verify contact emails are real
# Verify events make sense
```

---

## Performance Considerations

### Execution Time

**Expected pipeline execution:**
- Stage 1 (Discovery): ~5-10 seconds
- Stage 2 (Profiling per org): ~25-35 seconds each (crawling is slower but more thorough)
- **Total for 3 orgs:** ~90-120 seconds

**Note:** Crawling takes longer than single-page extraction but provides much better data coverage.

### Optimization Options

1. **Firebase Deduplication (CRITICAL for cost savings):**
   ```python
   # Before profiling each URL, check if already in database
   existing_org = await firestore.get_organization_by_url(url)
   if existing_org:
       print(f"⚡ Skipping {url} - already in database")
       organizations.append(existing_org)  # Reuse existing data
       continue
   ```
   - Prevents re-processing same organizations
   - Saves 80-90% of API costs during testing/demos
   - Essential for hackathon development

2. **Use Cost-Effective LLM Model:**
   ```python
   # Use gpt-4o-mini (cheaper, faster) instead of gpt-4
   model = "gpt-4o-mini"  # ~15x cheaper than gpt-4
   ```

3. **Parallel profiling:**
   ```python
   profiles = await asyncio.gather(*[
       profile_organization(url) for url in org_urls
   ])
   ```

4. **Rate limiting:**
   - Tavily: 100 requests/month free tier (crawl costs more credits than extract)
   - OpenAI: Monitor token usage (~1500 tokens per org for structuring)
   - Add exponential backoff for retries

### Credit Cost Analysis

**Per Organization:**
- Tavily Crawl: ~3 credits (2 for advanced extract + 1 for mapping with instructions, ~15 pages)
- OpenAI Structuring: ~$0.01 (1500 tokens with gpt-4o-mini)

**For 3 Organizations:**
- Tavily: ~9 credits total
- OpenAI: ~$0.03 total

**Comparison to Old Approach (Extract + OpenAI):**
- OLD: 1 Tavily credit + $0.01 OpenAI (single page extraction)
- NEW: 9 Tavily credits + $0.03 OpenAI (multi-page crawling)
- **Tradeoff:** 9x more expensive BUT much better data quality (contact info, events across multiple pages)

**Why This is Worth It:**
- Crawl checks contact page, events page, about page automatically
- Better chance of finding email and phone
- More complete event listings
- Less manual debugging of missing data

---

## Error Handling

### Common Errors

1. **No contact info found:**
   - Mark organization as "incomplete"
   - Don't save to database
   - Log for manual review

2. **Crawling failed:**
   - Retry with reduced depth (max_depth=1)
   - Fall back to simpler crawl (without instructions)
   - Last resort: try single-page extract
   - Skip if still failing

3. **Invalid website URL:**
   - Skip and continue with next org
   - Log the URL for review

4. **LLM returned invalid JSON:**
   - Retry with more explicit prompt
   - Use JSON schema validation
   - Fallback to manual parsing

### Error Response Format

```json
{
  "run_id": "run_xyz",
  "status": "partial_success",
  "organizations": [...],
  "errors": [
    {
      "url": "https://failed-org.se",
      "stage": "profiling",
      "error": "No contact information found"
    }
  ]
}
```

---

## Configuration

### Category Query Mapping

```python
CATEGORY_QUERIES = {
    "sports": "idrottsföreningar Stockholm ungdom",
    "youth_centers": "fritidsgård Stockholm verksamhet",
    "scouts": "scoutkårer Stockholm",
    "cultural": "kulturföreningar Stockholm barn",
    "educational": "studieförbund Stockholm ungdom"
}
```

### Validation Rules

```python
VALIDATION_RULES = {
    "required_fields": ["name", "website"],
    "required_contact": ["email", "phone"],  # At least one
    "min_events": 1,
    "age_range_min": 7,
    "age_range_max": 19
}
```

---

## Next Steps After Backend

Once backend is working:

1. **Pre-compute demo data:**
   ```bash
   python scripts/generate_demo_data.py
   # Saves to demo-data.json
   ```

2. **Test data quality:**
   - Manually verify emails are real
   - Check if events are current
   - Validate age ranges

3. **Document API:**
   - FastAPI auto-generates docs at `/docs`
   - Test all endpoints in Swagger UI

4. **Deploy (optional):**
   - Deploy to Railway, Render, or Cloud Run
   - Update frontend to use production URL

5. **Build Frontend:**
   - Use saved demo data initially
   - Connect to backend API later

---

## Success Criteria

Backend is ready when:

- ✅ Pipeline discovers 3 organizations consistently
- ✅ Each organization has valid contact email
- ✅ Each organization has 2-3 events extracted
- ✅ Events have proper age ranges (7-19)
- ✅ Data is saved to Firebase correctly
- ✅ API endpoints return expected responses
- ✅ Execution time < 90 seconds for 3 orgs
- ✅ Error handling works for edge cases

---

## Demo Data Example

Expected output structure:

```json
{
  "run_id": "demo_run_001",
  "status": "completed",
  "execution_time_seconds": 67.4,
  "organizations": [
    {
      "id": "org_001",
      "name": "Rinkeby IF",
      "type": "Sports Club",
      "website": "https://rinkebyif.se",
      "contact": {
        "email": "info@rinkebyif.se",
        "phone": "+46 8 123 4567"
      },
      "location": "Rinkeby, Stockholm",
      "description": "Youth sports club focusing on football and basketball",
      "events": [
        {
          "name": "Football Training",
          "type": "recurring",
          "schedule": "Mondays & Wednesdays 17:00-19:00",
          "age_range": "8-14",
          "description": "Regular training for youth teams"
        },
        {
          "name": "Summer Basketball Camp",
          "type": "one-time",
          "date": "2025-07-15",
          "age_range": "10-16",
          "description": "Week-long basketball intensive"
        }
      ]
    }
  ]
}
```

---

## Notes for GitHub Copilot

**When implementing:**

1. Use `async/await` for all external API calls
2. Add type hints to all functions
3. Use Pydantic models for data validation
4. Handle errors gracefully with try/except
5. Log important steps for debugging (especially crawl progress)
6. Use environment variables for all API keys
7. Follow FastAPI best practices for route handlers
8. Use dependency injection for database connections
9. **Use Tavily Crawl with instructions** for better multi-page data gathering
10. **Use OpenAI's `response_format=json_object`** for guaranteed JSON responses

**Code style:**
- Follow PEP 8
- Use descriptive variable names
- Add docstrings to all functions
- Keep functions small and focused
- Prefer composition over inheritance

**Security:**
- Never commit API keys or credentials
- Use `.env` for secrets
- Validate all user inputs
- Sanitize data before LLM prompts
- Use CORS properly for frontend access

---

End of specification. Ready for implementation.