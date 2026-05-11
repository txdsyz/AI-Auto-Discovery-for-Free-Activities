"""
Event Discovery Service
Discovers free youth sports events using SerpAPI search and AI extraction
"""
from typing import List, Dict, Any, Optional
import re
import os
import time
import json
import asyncio
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from app.integrations.openai import openai_client
from app.integrations.firebase import firestore_client
from app.config import settings


def generate_event_search_queries(city: str) -> List[str]:
    """
    Generate bilingual search queries for finding free youth sports events.
    
    Args:
        city: City name to search in
        
    Returns:
        List of search queries (up to 8)
    """
    en_templates = [
        "free youth {sport} clinic {city}",
        "free kids {sport} event {city}",
        "open {sport} session free {city}"
    ]
    sv_templates = [
        "gratis ungdoms {sport} träning {city}",
        "gratis barn {sport} aktivitet {city}",
        "öppen {sport} träning gratis {city}"
    ]
    sports_en = ["basketball", "soccer", "swimming", "tennis", "volleyball", "handball", "hockey"]
    sports_sv = ["basket", "fotboll", "simning", "tennis", "volleyboll", "handboll", "ishockey"]
    
    queries = set()
    for sport in sports_en:
        for template in en_templates:
            queries.add(template.format(sport=sport, city=city))
    for sport in sports_sv:
        for template in sv_templates:
            queries.add(template.format(sport=sport, city=city))
    
    return list(queries)[:8]


def is_valid_event_url(url: str) -> bool:
    """
    Check if URL is valid for event scraping.
    Filters out news sites, Wikipedia, Reddit, etc.
    """
    bad_domains = ["wikipedia.org", "reddit.com", "aftonbladet.se", "expressen.se"]
    return not any(bad in urlparse(url).netloc.lower() for bad in bad_domains)


def search_google_with_serpapi(query: str, serpapi_key: str, num_results: int = 3) -> List[str]:
    """
    Search Google using SerpAPI and return URLs.
    
    Args:
        query: Search query
        serpapi_key: SerpAPI API key
        num_results: Number of results to return
        
    Returns:
        List of URLs
    """
    try:
        response = requests.get("https://serpapi.com/search", params={
            "engine": "google",
            "q": query,
            "api_key": serpapi_key,
            "num": num_results,
            "gl": "se",
            "hl": "sv"
        }, timeout=10)
        
        urls = []
        for result in response.json().get("organic_results", []):
            url = result.get("link")
            if url and is_valid_event_url(url):
                urls.append(url)
        return urls
    except Exception as e:
        print(f"  [!] SerpAPI Error: {e}")
        return []


def extract_clean_text_from_url(url: str) -> str:
    """
    Scrape and clean text content from a URL using BeautifulSoup.
    
    Args:
        url: URL to scrape
        
    Returns:
        Cleaned text content (max 12000 chars)
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = response.apparent_encoding
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove unwanted tags
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()
        
        # Extract text
        text = soup.get_text(separator=" ", strip=True)
        return " ".join(text.split())[:12000]
    except Exception as e:
        print(f"  [!] Scrape Error for {url}: {e}")
        return ""


def extract_kfum_time(text: str) -> tuple:
    """
    Extract date and time from Swedish/English text patterns.
    
    Args:
        text: Raw text containing date/time information
        
    Returns:
        Tuple of (date_str, time_str) or (None, None)
    """
    text = text.replace(".", ":")
    month_map = {
        "januari": "01", "februari": "02", "mars": "03", "april": "04",
        "maj": "05", "juni": "06", "juli": "07", "augusti": "08",
        "september": "09", "oktober": "10", "november": "11", "december": "12",
        "january": "01", "february": "02", "march": "03", "april": "04",
        "may": "05", "june": "06", "july": "07", "august": "08",
        "september": "09", "october": "10", "november": "11", "december": "12"
    }
    
    # Match: June 23 – August 16, 9:00 – 16:30
    match = re.search(r"(?i)([a-zåäö]+)\s+(\d{1,2})\s*–", text)
    time_match = re.search(r"(\d{1,2}):(\d{2})", text)
    
    date_str = None
    if match and match.group(1).lower() in month_map:
        month = month_map[match.group(1).lower()]
        day = match.group(2).zfill(2)
        date_str = f"2025-{month}-{day}"
    
    time_str = None
    if time_match:
        h, m = time_match.groups()
        if 0 <= int(h) <= 23 and 0 <= int(m) <= 59:
            time_str = f"{int(h):02d}:{m}"
    
    return date_str, time_str


def extract_event_from_text(text: str, url: str, city: str) -> Optional[Dict[str, Any]]:
    """
    Extract structured event data from raw text using OpenAI.
    
    Args:
        text: Raw text content from webpage
        url: Source URL
        city: City name
        
    Returns:
        Structured event data or None if extraction fails
    """
    # Check if content mentions free/gratis
    text_lower = text.lower()
    if 'gratis' not in text_lower and 'free' not in text_lower and 'kostnadsfri' not in text_lower:
        return None
    
    prompt = f"""Extract as JSON. Summary in English. Use null if unknown.
Fields: title, sport_category, date (YYYY-MM-DD), time (HH:MM), location, age_group, is_free (boolean), summary, language ("en"/"sv")
Text: {text[:4000]}"""
    
    try:
        # Use async completion with JSON mode
        response_text = asyncio.run(openai_client.completion(
            prompt=prompt,
            response_format={"type": "json_object"}
        ))
        response = json.loads(response_text) if response_text else None
        
        if response and isinstance(response, dict):
            # Check if it's a free event
            if response.get('is_free') is False:
                return None
            
            # Ensure is_free is True and has title
            if (response.get('is_free') is True or response.get('is_free') is None) and response.get('title'):
                response['is_free'] = True
                response['source_url'] = url
                response['city'] = city
                
                # Clean up date/time fields
                if response.get('date') == 'null' or not response.get('date'):
                    response['date'] = None
                if response.get('time') == 'null' or not response.get('time'):
                    response['time'] = None
                
                return response
    
    except Exception as e:
        print(f"  ⚠️ OpenAI extraction failed: {e}")
    
    return None


def fallback_event_extraction(text: str, url: str, city: str) -> Optional[Dict[str, Any]]:
    """
    Fallback extraction using regex patterns when AI fails.
    
    Args:
        text: Raw text content
        url: Source URL
        city: City name
        
    Returns:
        Basic event data or None
    """
    text_lower = text.lower()
    
    # Must mention free/gratis
    if 'gratis' not in text_lower and 'free' not in text_lower:
        return None
    
    # Extract title from first meaningful line
    lines = [ln.strip() for ln in text[:1000].split('\n') if len(ln.strip()) > 20]
    title = (lines[0] if lines else "Free Activity")[:100]
    
    # Try to detect specific locations
    location = city
    for loc in ["Rosengatan", "Löten", "Fyrishov", "Studenternas"]:
        if loc in text:
            location = f"{loc}, {city}"
            break
    
    # Detect sport category
    sport_keywords = {
        'basketball': ['basket', 'basketball'],
        'soccer': ['fotboll', 'soccer', 'football'],
        'swimming': ['simning', 'swimming', 'swim'],
        'tennis': ['tennis'],
        'volleyball': ['volleyboll', 'volleyball'],
        'handball': ['handboll', 'handball'],
        'hockey': ['hockey', 'ishockey'],
    }
    
    sport_category = 'multiple'
    for sport, keywords in sport_keywords.items():
        if any(kw in text_lower for kw in keywords):
            sport_category = sport
            break
    
    age_group = "all children and youth"
    language = 'sv' if 'gratis' in text_lower else 'en'
    
    # Extract date and time
    date, time_str = extract_kfum_time(text)
    
    # Default to summer if summer keywords found
    if not date and ("sommarlov" in text_lower or "summer" in text_lower):
        date = "2025-06-23"
    
    return {
        'title': title,
        'sport_category': sport_category,
        'date': date,
        'time': time_str,
        'location': location,
        'age_group': age_group,
        'is_free': True,
        'summary': 'Free drop-in sports for all children and youth. No registration required.',
        'language': language,
        'source_url': url,
        'city': city,
        '_fallback': True
    }


def discover_events_for_city(city: str, max_events: int = 10) -> Dict[str, Any]:
    """
    Discover free youth sports events for a specific city using SerpAPI.
    
    Args:
        city: City name to search in
        max_events: Maximum number of events to discover
        
    Returns:
        Discovery results with events found and saved
    """
    print(f"\n� Fetching free youth sports activities in {city}...")
    print(f"   Max events: {max_events}")
    
    # Get SerpAPI key
    serpapi_key = os.getenv("SERPAPI_API_KEY")
    if not serpapi_key:
        print("❌ Error: SERPAPI_API_KEY not found in environment")
        return {
            'run_id': 'error',
            'status': 'failed',
            'city': city,
            'events_found': 0,
            'events_saved': 0,
            'started_at': datetime.utcnow().isoformat(),
            'completed_at': datetime.utcnow().isoformat()
        }
    
    run_id = f"event_discovery_{city.lower()}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    started_at = datetime.utcnow()
    
    # Generate search queries
    queries = generate_event_search_queries(city)
    print(f"   Generated {len(queries)} search queries\n")
    
    # Search and extract events
    discovered_events = []
    processed_urls = set()
    
    for query in queries:
        if len(discovered_events) >= max_events:
            break
        
        print(f"  → Searching: {query}")
        
        try:
            # Search using SerpAPI
            urls = search_google_with_serpapi(query, serpapi_key, num_results=3)
            
            if not urls:
                continue
            
            # Process each URL
            for url in urls:
                if len(discovered_events) >= max_events:
                    break
                
                # Skip duplicates
                if url in processed_urls:
                    continue
                
                processed_urls.add(url)
                
                # Scrape webpage content
                raw_text = extract_clean_text_from_url(url)
                
                if not raw_text or len(raw_text) < 300:
                    continue
                
                print(f"     • Processing: {url[:60]}...")
                
                # Try AI extraction first
                event_data = extract_event_from_text(raw_text, url, city)
                
                # Fallback to regex extraction
                if not event_data:
                    print("       ⚠️ Using fallback")
                    event_data = fallback_event_extraction(raw_text, url, city)
                
                if event_data and event_data.get('title'):
                    discovered_events.append(event_data)
                    print(f"       ✓ Extracted: {event_data['title'][:50]}")
            
            # Rate limiting
            time.sleep(0.8)
        
        except Exception as e:
            print(f"     ✗ Search failed: {e}")
            continue
    
    # Save events to Firebase
    events_saved = 0
    for event_data in discovered_events:
        try:
            firestore_client.save_event(event_data)
            events_saved += 1
        except Exception as e:
            print(f"  ✗ Failed to save event: {e}")
    
    completed_at = datetime.utcnow()
    
    result = {
        'run_id': run_id,
        'status': 'completed',
        'city': city,
        'events_found': len(discovered_events),
        'events_saved': events_saved,
        'started_at': started_at.isoformat(),
        'completed_at': completed_at.isoformat()
    }
    
    print(f"\n✅ Event discovery completed!")
    print(f"   Events found: {len(discovered_events)}")
    print(f"   Events saved: {events_saved}")
    
    return result
