"""
Stage 1: Organization Discovery Service
Discovers youth organizations using web search with diverse strategies
"""
from typing import List, Set, Dict, Any
from app.config import settings
from app.integrations.tavily import tavily_client


# Stockholm neighborhoods for targeted searches
STOCKHOLM_AREAS = [
    "Södermalm", "Östermalm", "Kungsholmen", "Vasastan", "Norrmalm",
    "Rinkeby", "Tensta", "Husby", "Årsta", "Enskede", "Hägersten",
    "Farsta", "Skärholmen", "Älvsjö", "Bromma", "Hässelby", "Spånga"
]

# Diverse search patterns to find different types of organizations
SEARCH_PATTERNS = {
    "sports": [
        "{area} idrottsförening ungdom",  # Sports club youth
        "{area} fotbollsklubb barn",      # Football club children
        "{area} friidrott ungdom",        # Athletics youth
        "ungdomsidrott {area} Stockholm", # Youth sports
    ],
    "youth_centers": [
        "{area} ungdomsgård Stockholm",   # Youth center
        "{area} fritidsgård barn",        # Recreation center
        "fritidsverksamhet {area}",       # Leisure activities
    ],
    "scouts": [
        "{area} scoutkår Stockholm",      # Scout troop
        "scouter {area} barn ungdom",     # Scouts children youth
    ],
    "cultural": [
        "{area} kulturförening ungdom",   # Cultural association
        "{area} musikskola barn",         # Music school
        "{area} teater ungdom",           # Theater youth
    ]
}


async def discover_organizations(
    search_query: str = None,
    categories: List[str] = None, 
    max_orgs: int = 3,
    diversify: bool = True
) -> List[Dict[str, Any]]:
    """
    Discover organization URLs using search query or category-based strategies.
    
    Strategy to get NEW organizations each time:
    1. Use custom search query (preferred) OR rotate through categories/neighborhoods
    2. Filter out previously seen domains
    3. Prioritize organizations with actual domain names (not umbrella orgs)
    
    Args:
        search_query: Direct search query (e.g., "Södermalm idrottsförening ungdom")
        categories: List of category names (e.g., ["sports", "youth_centers"]) - used if no search_query
        max_orgs: Maximum number of organizations to discover
        diversify: If True, use varied search patterns across neighborhoods
        
    Returns:
        List of dicts with URL and discovery metadata:
        [
            {
                "url": "https://example.se",
                "category": "custom" or category name,
                "search_query": "query used",
                "search_score": 0.89
            }
        ]
        
    Example:
        orgs = await discover_organizations(search_query="Södermalm idrottsförening ungdom", max_orgs=5)
        for org in orgs:
            print(f"{org['url']} found via {org['search_query']}")
    """
    all_results: List[Dict[str, Any]] = []
    seen_domains: Set[str] = set()
    
    # If custom search query provided, use it directly
    if search_query:
        print(f"🔍 Discovering {max_orgs} organizations with custom query: '{search_query}'")
        results = await _search_with_filters(search_query, seen_domains, category="custom")
        all_results.extend(results[:max_orgs])
    # Otherwise use category-based search
    elif categories:
        print(f"🔍 Discovering {max_orgs} organizations across categories: {categories}")
        
        for category in categories:
            print(f"\n📂 Category: {category}")
            
            if diversify and category in SEARCH_PATTERNS:
                # Use diverse search patterns across different areas
                patterns = SEARCH_PATTERNS[category]
                areas_to_search = STOCKHOLM_AREAS[:3]  # Rotate through 3 areas
                
                for area in areas_to_search:
                    for pattern in patterns[:2]:  # Use 2 patterns per area
                        query = pattern.format(area=area)
                        results = await _search_with_filters(query, seen_domains, category)
                        all_results.extend(results)
                        
                        if len(all_results) >= max_orgs:
                            break
                    if len(all_results) >= max_orgs:
                        break
            else:
                # Use default category query
                query = settings.CATEGORY_QUERIES.get(category, f"{category} Stockholm ungdom")
                results = await _search_with_filters(query, seen_domains, category)
                all_results.extend(results)
    
    # Sort by relevance score and filter
    all_results.sort(key=lambda x: x.get('score', 0), reverse=True)
    
    # Extract unique URLs with metadata, filtering out umbrella organizations
    unique_orgs = []
    for result in all_results:
        url = result.get('url', '')
        domain = _extract_domain(url)
        
        # Skip if already seen or is an umbrella org
        if domain in seen_domains or _is_umbrella_org(url, result.get('content', '')):
            continue
        
        seen_domains.add(domain)
        
        # Build organization discovery record with metadata
        org_record = {
            'url': url,
            'category': result.get('category'),
            'search_query': result.get('search_query'),
            'search_score': result.get('score', 0),
            'discovered_at': result.get('discovered_at')
        }
        unique_orgs.append(org_record)
        
        if len(unique_orgs) >= max_orgs:
            break
    
    print(f"\n✅ Discovered {len(unique_orgs)} unique organization URLs")
    for i, org in enumerate(unique_orgs, 1):
        print(f"   {i}. {org['url']} (via {org['category']})")
    
    return unique_orgs


async def _search_with_filters(query: str, seen_domains: Set[str], category: str) -> List[Dict[str, Any]]:
    """
    Search with filters to find actual youth organizations.
    Adds category and query metadata to each result.
    """
    print(f"   🔎 Query: '{query}'")
    
    try:
        results = await tavily_client.search(
            query=query,
            max_results=5,
            search_depth="advanced",
            include_domains=[".se"]  # Only Swedish sites
        )
        
        # Filter results and add metadata
        from datetime import datetime
        filtered = []
        for result in results:
            url = result.get('url', '')
            domain = _extract_domain(url)
            
            # Skip if already seen
            if domain in seen_domains:
                continue
            
            # Check if it looks like an actual organization
            if _looks_like_org_website(url):
                # Add discovery metadata
                result['category'] = category
                result['search_query'] = query
                result['discovered_at'] = datetime.utcnow().isoformat()
                filtered.append(result)
        
        print(f"      Found {len(filtered)} new results")
        return filtered
        
    except Exception as e:
        print(f"      ❌ Search failed: {e}")
        return []


def _extract_domain(url: str) -> str:
    """Extract domain from URL for deduplication."""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc.lower()
    except:
        return url


def _looks_like_org_website(url: str) -> bool:
    """
    Check if URL looks like an actual organization website.
    Filter out umbrella orgs, government sites, directories.
    """
    url_lower = url.lower()
    
    # Exclude umbrella/support organizations
    exclude_keywords = [
        'rfsisu', 'rf.se', 'sisuidrottsutbildarna',  # Sports federations
        'aktivungdom.se',  # Activity directories
        'stockholm.se', 'regeringen.se',  # Government
        'wikipedia', 'facebook', 'instagram',  # Social media
    ]
    
    for keyword in exclude_keywords:
        if keyword in url_lower:
            return False
    
    # Prefer actual organization domains (shorter, simpler)
    # Good: rinkebyif.se, skaikesida.se
    # Bad: www.rfsisu.se/distrikt/stockholm/...
    domain = _extract_domain(url)
    parts = domain.split('.')
    
    # Simple domain structure is better (org.se)
    if len(parts) <= 3:
        return True
    
    return True  # Allow others but with lower priority


def _is_umbrella_org(url: str, content: str) -> bool:
    """
    Check if this is an umbrella/support organization based on URL and content.
    """
    # Check URL patterns
    if not _looks_like_org_website(url):
        return True
    
    # Check content keywords
    content_lower = content.lower()
    umbrella_indicators = [
        'distrikt',  # District organization
        'förbund',  # Federation
        'stödjer föreningar',  # Supports clubs
        'utvecklar idrotten',  # Develops sports
    ]
    
    matches = sum(1 for indicator in umbrella_indicators if indicator in content_lower)
    return matches >= 2  # If 2+ indicators, likely umbrella org
