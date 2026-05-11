"""
LLM Prompt Templates for Youth Organization Discovery Pipeline

This file contains:
1. CRAWL_INSTRUCTIONS - Guide Tavily crawl to find relevant data across multiple pages
2. STRUCTURE_PROMPT - Convert crawled content into structured JSON
3. VALIDATION_PROMPT - Validate extracted organization data
"""

# ==============================================================================
# TAVILY CRAWL INSTRUCTIONS
# ==============================================================================

# ===========================
# TAVILY CRAWL INSTRUCTIONS
# ===========================
# Note: Tavily API has a 400 character limit for instructions
# PRIORITY: Contact info first, then events

CRAWL_INSTRUCTIONS = """
Swedish youth org (ages 7-19). PRIORITY:
1. Contact: email, phone (check Kontakt, footer, Om oss pages)
2. What they do for youth
3. Events/activities: name, age, schedule
Search: Kontakt, E-post, Telefon, Barn, Ungdom, Verksamhet
"""

# ==============================================================================
# OPENAI STRUCTURING PROMPT
# ==============================================================================

STRUCTURE_PROMPT = """
Extract data from Swedish youth organization website (ages 7-19).

Content:
{content}

If NOT a youth org (umbrella org, training provider, directory, government), return:
{{"relevant": false, "reason": "why"}}

Otherwise return:
{{
  "relevant": true,
  "name": "Organization name",
  "type": "Sports Club/Youth Center/Scout Group/Cultural",
  "category": "ONE of: sports, youth_centers, scouts, cultural, education, religious, community, other",
  "contact": {{"email": "email or null", "phone": "phone or null"}},
  "location": "Specific neighborhood/area (e.g. 'Södermalm, Stockholm' or 'Rinkeby' or 'Tensta') or null",
  "description": "What they do for youth (one sentence)",
  "events": [
    {{"name": "event name", "type": "recurring/one-time", "schedule": "day+time or null", "date": "YYYY-MM-DD or null", "age_range": "e.g. 8-14 or null", "description": "brief"}}
  ]
}}

LOCATION EXTRACTION (IMPORTANT):
- Find the SPECIFIC neighborhood/area name (Södermalm, Östermalm, Rinkeby, Tensta, etc.)
- Look for: "Besöksadress:", "Adress:", "Plats:", physical address, neighborhood mentions
- Return format: "Neighborhood" or "Neighborhood, Stockholm" (be specific, not just "Stockholm")
- If only "Stockholm" found without specific area, return "Stockholm"
- If no location found, return null

CATEGORY DETERMINATION:
- sports: Football clubs, basketball, athletics, swimming, general sports associations
- youth_centers: Fritidsgård, ungdomsgård, recreation centers
- scouts: Scouting organizations (Scoutkår)
- cultural: Music schools, theater groups, art programs, dance
- education: Tutoring, study help, after-school programs
- religious: Church youth groups, faith-based organizations
- community: Neighborhood associations, integration programs
- other: Doesn't fit above categories

CONTACT EXTRACTION (CRITICAL):
- Email: Look for patterns like name@domain.se, info@..., kontakt@..., or text like "E-post:", "Mejla:"
- Phone: Swedish format +46..., 08-..., 070-..., or text like "Telefon:", "Ring:"
- Search ALL sections, especially pages with "kontakt", "om oss", "footer" content
- If contact form only (no direct email), use null

PRIORITY: 1.Contact info 2.Location 3.Category 4.Youth focus 5.Events (1-3 if found, [] if none)

Return ONLY valid JSON, no markdown.
"""

# ==============================================================================
# LEGACY PROMPT (Keep for backward compatibility if needed)
# ==============================================================================

ORGANIZATION_PROFILE_PROMPT = """
[DEPRECATED - Use CRAWL_INSTRUCTIONS + STRUCTURE_PROMPT instead]

You are analyzing a Swedish youth organization's website to extract structured data.

Website URL: {url}
Website Content:
{content}

Extract the following information and return as valid JSON:

{{
  "name": "Organization name",
  "type": "Organization type",
  "contact": {{"email": "email", "phone": "phone"}},
  "location": "Location in Stockholm",
  "description": "One sentence description",
  "events": [{{"name": "", "type": "", "schedule": "", "date": "", "age_range": "", "description": ""}}]
}}

Return ONLY valid JSON.
"""

# ==============================================================================
# VALIDATION PROMPT
# ==============================================================================


VALIDATION_PROMPT = """
Review the extracted organization data and verify it meets all requirements.

Extracted Data:
{data}

Check the following:
1. Does it have a valid email address?
2. Are there at least 2 events listed?
3. Are age ranges appropriate for youth (7-19)?
4. Is the location specific (not just "Stockholm")?

Return JSON:
{{
  "valid": true/false,
  "issues": ["list of any issues found"],
  "suggestions": ["list of suggestions for improvement"]
}}
"""
