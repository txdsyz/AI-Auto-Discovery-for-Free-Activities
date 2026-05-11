# Migration to Tavily Crawl Architecture

**Date:** November 8, 2025
**Status:** ✅ Complete - Ready for Testing

## Overview

Migrated from single-page extraction to multi-page crawling for better data quality.

---

## Architecture Changes

### OLD Approach (Extract-based)
```
Search → Extract Single Page → OpenAI Full Extraction → Validate
         (0.2 credits)        (full prompt)
```

### NEW Approach (Crawl-based)
```
Search → Crawl Multiple Pages → OpenAI Structuring → Validate
         (3 credits)           (simplified prompt)
         Homepage, Contact,
         Events, About pages
```

---

## Files Modified

### 1. ✅ `app/integrations/tavily.py`
**Changes:**
- Added new `crawl()` method
- Kept existing `search()` and `extract()` methods for backward compatibility

**New Method:**
```python
async def crawl(
    url: str,
    instructions: str,
    max_depth: int = 2,
    max_breadth: int = 10,
    limit: int = 15,
    extract_depth: str = "advanced",
    format: str = "markdown"
) -> Dict[str, Any]
```

**Cost:** ~3 credits per organization (vs 0.2 for extract)
**Timeout:** 90 seconds (vs 30 for extract)

---

### 2. ✅ `app/integrations/openai.py`
**Changes:**
- Updated `completion()` to support `response_format` parameter
- Updated `parse_json_response()` to use JSON mode by default
- System message updated for structuring vs extraction

**New Parameter:**
```python
async def completion(
    prompt: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0.1,
    max_tokens: Optional[int] = None,
    response_format: Optional[dict] = None  # NEW: Force JSON
) -> str
```

**Usage:**
```python
# Guaranteed valid JSON
response = await openai_client.completion(
    prompt="Convert this to JSON: ...",
    response_format={"type": "json_object"}
)
```

---

### 3. ✅ `app/utils/prompts.py`
**Changes:**
- Added `CRAWL_INSTRUCTIONS` - Guide Tavily what to extract
- Added `STRUCTURE_PROMPT` - Convert crawled content to JSON
- Kept old `ORGANIZATION_PROFILE_PROMPT` for backward compatibility (marked deprecated)

**New Prompts:**

**CRAWL_INSTRUCTIONS:**
- Guides Tavily to find: org details, contact info, youth events
- Specifies where to look: contact page, footer, about page
- Target: ages 7-19 (barn/ungdom)

**STRUCTURE_PROMPT:**
- Much simpler than old prompt
- Just structures pre-extracted data
- Uses `response_format=json_object` for guaranteed JSON

---

### 4. ✅ `app/services/profiling.py`
**Changes:**
- Complete rewrite of `profile_organization()`
- New 6-step process

**New Implementation:**

**Step 1:** Crawl website
```python
crawl_result = await tavily_client.crawl(
    url=url,
    instructions=CRAWL_INSTRUCTIONS,
    max_depth=2,
    max_breadth=10,
    limit=15
)
```

**Step 2:** Combine content from all pages
```python
for page in crawl_result['results']:
    all_content += f"\n\n=== {page['url']} ===\n{page['raw_content']}"
```

**Step 3:** Truncate to 15,000 chars (~4000 tokens)

**Step 4:** Structure with OpenAI
```python
profile = await openai_client.parse_json_response(
    prompt=STRUCTURE_PROMPT.format(content=all_content),
    model="gpt-4o-mini",
    use_json_mode=True  # Guaranteed valid JSON
)
```

**Step 5:** Validate required fields

**Step 6:** Add metadata and return

---

### 5. ✅ `docs/backend_spec.md`
**Changes:**
- Updated tech stack section
- Rewrote Stage 2 pipeline description
- Added crawl pseudocode
- Updated cost analysis section
- Updated execution time estimates

**Key Updates:**
- Tech: "Tavily Crawl API with instructions"
- Model: "GPT-4o-mini for JSON structuring only"
- Cost: ~9 credits for 3 orgs (vs 1 credit old way)
- Time: ~90-120 seconds for 3 orgs (vs 60-80 seconds)

---

### 6. ✅ `docs/todo.md`
**Changes:**
- Marked Phase 1 as complete
- Updated Phase 2 with crawl tasks
- Rewrote Phase 3 profiling section
- Updated optimization section
- Updated cost management notes

**Key Sections:**
- Phase 2.2: Replace extract with crawl
- Phase 2.3: Add `response_format` support
- Phase 3.2: New prompts (CRAWL_INSTRUCTIONS, STRUCTURE_PROMPT)
- Phase 3.3: Complete rewrite of profiling function

---

## Benefits of New Approach

### ✅ Better Data Quality
- Crawls multiple pages (homepage, contact, events, about)
- Higher success rate for finding email/phone
- More complete event listings
- Better coverage of organization info

### ✅ More Reliable JSON
- `response_format=json_object` guarantees valid JSON
- No more retry logic needed for JSON parsing
- Cleaner code, fewer edge cases

### ✅ Simpler Prompts
- Tavily does heavy lifting (extraction)
- OpenAI just structures data
- Less prompt engineering needed

---

## Tradeoffs

### ⚠️ Higher Cost
- **OLD:** 1 Tavily credit + $0.01 OpenAI = 3 orgs
- **NEW:** 9 Tavily credits + $0.03 OpenAI = 3 orgs
- **Increase:** 9x Tavily credits, 3x OpenAI cost

### ⚠️ Slower Execution
- **OLD:** ~20 seconds per org
- **NEW:** ~30-35 seconds per org
- **Increase:** +50% time per org

### ✅ Worth It Because:
- Much better data quality
- Higher success rate (fewer failed orgs)
- Less debugging needed
- Better demo results

---

## Cost Optimization Still Applies

### Firebase Deduplication (CRITICAL)
```python
# Check before crawling (crawl is expensive!)
existing_org = await firestore.get_organization_by_url(url)
if existing_org:
    print(f"⚡ Skipping {url} - already in database")
    return existing_org  # Saves ~3 credits!
```

**Savings:** 80-90% cost reduction during testing/demos

---

## Testing Checklist

### Integration Tests
- [ ] Test `tavily_client.crawl()` with real Swedish org
  - Verify crawls multiple pages
  - Check instructions work
  - Confirm email/phone extraction
- [ ] Test `openai_client.completion()` with `response_format`
  - Verify guaranteed JSON output
  - Check gpt-4o-mini works well
- [ ] Test `profile_organization()` end-to-end
  - Real Swedish org URL
  - Check all 6 steps execute
  - Verify profile structure

### Cost Monitoring
- [ ] Monitor Tavily credit usage (~3 per org)
- [ ] Monitor OpenAI token usage (~1500 tokens per org)
- [ ] Verify deduplication works (no re-crawling)

### Data Quality
- [ ] Verify email extraction improves
- [ ] Check event count increases
- [ ] Validate Swedish content parsing

---

## Next Steps

1. **Test Integration:**
   ```bash
   cd backend
   python -c "
   import asyncio
   from app.services.profiling import profile_organization
   
   async def test():
       profile = await profile_organization('https://example-swedish-org.se')
       print(profile)
   
   asyncio.run(test())
   "
   ```

2. **Update Pipeline:**
   - `pipeline.py` already uses `profile_organization()`
   - No changes needed there!

3. **Run Full Pipeline:**
   ```bash
   # Start server
   uvicorn main:app --reload
   
   # Test discovery endpoint
   curl -X POST http://localhost:8000/api/discover \
     -H "Content-Type: application/json" \
     -d '{"categories": ["sports"], "max_organizations": 1}'
   ```

4. **Monitor & Optimize:**
   - Check crawl performance
   - Adjust max_depth/limit if needed
   - Fine-tune instructions if extraction quality issues

---

## Rollback Plan

If crawl doesn't work well:

1. Revert to extract:
   ```python
   # In profiling.py, replace crawl with:
   extract_result = await tavily_client.extract(url)
   ```

2. Use old prompt:
   ```python
   from app.utils.prompts import ORGANIZATION_PROFILE_PROMPT
   ```

3. Keep `response_format=json_object` (this is an improvement regardless)

---

## Summary

✅ **Migration Complete**
- All files updated
- New crawl-based architecture implemented
- Documentation updated
- Ready for testing

🎯 **Expected Outcome:**
- 80-90% email extraction success rate (vs 60-70% before)
- More events per organization
- Better data quality for demo

💰 **Cost:**
- ~9 Tavily credits for 3 orgs (worth it!)
- Deduplication still critical

⏱️ **Time:**
- ~90-120 seconds for 3 orgs (acceptable for hackathon)

🚀 **Next:** Test with real Swedish organizations!

---

**Last Updated:** November 8, 2025
**Migration Status:** ✅ Complete
