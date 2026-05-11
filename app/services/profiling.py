"""
Stage 2: Organization Profiling Service
Profiles organizations using Tavily Crawl + OpenAI structuring

NEW APPROACH:
1. Use Tavily Crawl to visit multiple pages (homepage, contact, events, about)
2. Combine content from all crawled pages
3. Use OpenAI to structure the combined content into JSON
"""
from typing import Dict, Any
from datetime import datetime
from app.integrations.tavily import tavily_client
from app.integrations.openai import openai_client
from app.utils.prompts import CRAWL_INSTRUCTIONS, STRUCTURE_PROMPT
from app.config import settings
import json


async def profile_organization(url: str, discovery_metadata: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Profile an organization using Tavily Crawl + OpenAI structuring.
    
    This function:
    1. Crawls the organization's website (multiple pages)
    2. Combines content from all pages
    3. Uses OpenAI to structure data into JSON
    4. Validates required fields
    5. Adds discovery metadata (category, search query)
    
    Args:
        url: Organization website URL
        discovery_metadata: Optional dict with category, search_query, etc.
        
    Returns:
        Dictionary containing organization profile with events and metadata
        
    Raises:
        ValueError: If required fields are missing or crawl fails
        Exception: If API calls fail
        
    Example:
        profile = await profile_organization("https://rinkebyif.se")
        # Returns: {
        #     "name": "Rinkeby IF",
        #     "type": "Sports Club",
        #     "contact": {"email": "info@rinkebyif.se", "phone": "+46 8..."},
        #     "location": "Rinkeby, Stockholm",
        #     "description": "...",
        #     "events": [...]
        # }
    """
    print(f"📍 Profiling organization: {url}")
    
    try:
        # STEP 1: Crawl the website with instructions
        print(f"🕷️  Crawling website (multi-page)...")
        crawl_result = await tavily_client.crawl(
            url=url,
            instructions=CRAWL_INSTRUCTIONS,
            max_depth=2,        # Crawl 2 levels deep
            max_breadth=10,     # Check up to 10 pages per level
            limit=15,           # Total pages to process
            extract_depth="advanced",
            format="markdown"
        )
        
        # STEP 2: Organize content in strategic order
        # Priority order: Homepage → Contact → Events → Other pages
        homepage_content = ""
        contact_content = ""
        events_content = ""
        other_content = ""
        page_count = 0
        
        # Page classification keywords
        contact_keywords = ['kontakt', 'contact', 'om-oss', 'om_oss', 'about']
        events_keywords = ['aktivitet', 'event', 'kalender', 'schema', 'program', 'verksamhet']
        
        for page in crawl_result.get('results', []):
            page_url = page.get('url', '').lower()
            page_content = page.get('raw_content') or ''
            
            if not page_content:
                continue
            
            page_count += 1
            formatted_page = f"\n\n{'='*80}\nPAGE: {page.get('url', '')}\n{'='*80}\n{page_content}"
            
            # Classify the page
            is_homepage = page_url == url.lower() or page_url.rstrip('/') == url.lower().rstrip('/')
            is_contact = any(keyword in page_url for keyword in contact_keywords)
            is_events = any(keyword in page_url for keyword in events_keywords)
            
            if is_homepage:
                homepage_content += formatted_page
                print(f"   🏠 Homepage: {page.get('url', '')}")
            elif is_contact:
                contact_content += formatted_page
                print(f"   � Contact page: {page.get('url', '')}")
            elif is_events:
                events_content += formatted_page
                print(f"   📅 Events page: {page.get('url', '')}")
            else:
                other_content += formatted_page
                print(f"   📄 Other page: {page.get('url', '')}")
        
        # Combine in strategic order: Homepage → Contact → Events → Other
        all_content = homepage_content + contact_content + events_content + other_content
        
        if not all_content:
            raise ValueError(f"No content extracted from {url}")
        
        print(f"📄 Crawled {page_count} pages, total content length: {len(all_content)} chars")
        
        # STEP 3: Truncate if too long (priority pages are at top, safe from truncation)
        max_content_length = 25000  # ~6500 tokens (increased from 15k)
        if len(all_content) > max_content_length:
            all_content = all_content[:max_content_length]
            print(f"⚠️  Content truncated to {max_content_length} chars (contact pages preserved)")
        
        # STEP 4: Use OpenAI to structure the crawled data
        print(f"🤖 Structuring data with OpenAI (gpt-4o-mini)...")
        prompt = STRUCTURE_PROMPT.format(content=all_content)
        
        # Use response_format=json_object for guaranteed valid JSON
        profile = await openai_client.parse_json_response(
            prompt=prompt,
            model="gpt-4o-mini",
            use_json_mode=True  # Guarantees valid JSON
        )
        
        # STEP 4.5: Check if organization is relevant
        if not profile.get('relevant', True):
            reason = profile.get('reason', 'Not a youth organization')
            print(f"⏭️  Skipping irrelevant organization: {url}")
            print(f"   Reason: {reason}")
            raise ValueError(f"IRRELEVANT: {reason}")
        
        # STEP 5: Validate required fields
        if not profile.get('name'):
            raise ValueError(f"Missing organization name for {url}")
        
        # Contact information - WARN if missing but continue
        # (Users can visit website directly to find contact info)
        contact = profile.get('contact', {})
        has_email = bool(contact.get('email'))
        has_phone = bool(contact.get('phone'))
        
        if not has_email and not has_phone:
            print(f"⚠️  WARNING: No direct contact info found for {profile.get('name')}")
            print(f"   → Users can visit website: {url}")
        elif not has_email:
            print(f"⚠️  WARNING: No email found for {profile.get('name')} - phone only: {contact.get('phone')}")
        
        # Check for events - warn if missing
        events = profile.get('events', [])
        if len(events) == 0:
            print(f"⚠️  WARNING: No events found for {profile.get('name')}")
            print(f"   → Check if organization description mentions youth activities")
        
        # STEP 6: Add metadata
        profile['website'] = url
        profile['created_at'] = datetime.utcnow().isoformat()
        profile['last_updated'] = datetime.utcnow().isoformat()
        
        # Add discovery metadata (how we found this organization)
        # Use LLM-determined category if available, otherwise use discovery category
        llm_category = profile.get('category')
        discovery_category = discovery_metadata.get('category') if discovery_metadata else None
        
        # Priority: LLM category > discovery category
        final_category = llm_category or discovery_category or 'other'
        
        if discovery_metadata:
            profile['discovery'] = {
                'category': final_category,
                'search_query': discovery_metadata.get('search_query'),
                'search_score': discovery_metadata.get('search_score'),
                'discovered_at': discovery_metadata.get('discovered_at')
            }
        else:
            # No discovery metadata, create minimal discovery info with LLM category
            profile['discovery'] = {
                'category': final_category,
                'search_query': None,
                'search_score': None,
                'discovered_at': datetime.utcnow().isoformat()
            }
        
        # Remove category from root level (it's in discovery metadata now)
        if 'category' in profile:
            del profile['category']
        
        print(f"✅ Successfully profiled: {profile['name']}")
        print(f"   📂 Category: {final_category}")
        print(f"   🏢 Type: {profile.get('type', 'N/A')}")
        print(f"   � Location: {profile.get('location', 'N/A')}")
        print(f"   �📧 Email: {contact.get('email', 'Not found - check website')}")
        print(f"   📞 Phone: {contact.get('phone', 'Not found - check website')}")
        print(f"   📝 Description: {profile.get('description', 'N/A')[:100]}...")
        print(f"   🎯 Events: {len(events)} activities found")
        
        return profile
        
    except Exception as e:
        print(f"❌ Failed to profile {url}: {str(e)}")
        raise


def validate_profile(profile: Dict[str, Any]) -> bool:
    """
    Validate that a profile has all required fields and correct data.
    
    Args:
        profile: Organization profile dictionary
        
    Returns:
        True if valid, raises ValueError if invalid
    """
    # Required fields
    if not profile.get('name'):
        raise ValueError("Missing required field: name")
    
    # At least one contact method required
    contact = profile.get('contact', {})
    if not contact.get('email') and not contact.get('phone'):
        raise ValueError("At least one contact method (email or phone) required")
    
    # Email is critical
    if not contact.get('email'):
        raise ValueError("Email is CRITICAL and must be present")
    
    # At least one event required
    events = profile.get('events', [])
    if len(events) < 1:
        raise ValueError("At least one event is required")
    
    # Validate age ranges (should be for youth: 7-19)
    for event in events:
        age_range = event.get('age_range', '')
        # Simple validation - can be enhanced
        if not age_range:
            raise ValueError(f"Event '{event.get('name')}' missing age_range")
    
    return True
