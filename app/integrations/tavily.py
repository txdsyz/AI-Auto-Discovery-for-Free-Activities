"""
Tavily API client for web search and content extraction.
"""

import httpx
from typing import List, Dict, Optional
from app.config import settings


class TavilyClient:
    """Client for interacting with Tavily API."""
    
    def __init__(self):
        self.api_key = settings.TAVILY_API_KEY
        self.base_url = "https://api.tavily.com"
        self.headers = {
            "Content-Type": "application/json"
        }
    
    async def search(
        self,
        query: str,
        max_results: int = 5,
        search_depth: str = "advanced",
        include_domains: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Search the web using Tavily API.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            search_depth: "basic" or "advanced"
            include_domains: List of domains to prioritize (e.g., [".se"])
        
        Returns:
            List of search results with url, title, and content
        """
        url = f"{self.base_url}/search"
        
        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": search_depth,
            "max_results": max_results,
        }
        
        if include_domains:
            payload["include_domains"] = include_domains
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(url, json=payload, headers=self.headers)
                
                # Handle error status codes
                if response.status_code == 401:
                    raise Exception("Invalid Tavily API key")
                elif response.status_code == 429:
                    raise Exception("Tavily API rate limit exceeded")
                elif response.status_code == 432:
                    raise Exception("Tavily API usage limit exceeded")
                elif response.status_code == 433:
                    raise Exception("Tavily API monthly limit exceeded")
                elif response.status_code == 500:
                    raise Exception("Tavily API server error")
                elif response.status_code != 200:
                    raise Exception(f"Tavily API error: {response.status_code} - {response.text}")
                
                data = response.json()
                return data.get("results", [])
                
            except httpx.TimeoutException:
                raise Exception("Tavily search request timed out")
            except httpx.RequestError as e:
                raise Exception(f"Tavily search request failed: {str(e)}")
    
    async def extract(
        self,
        urls: List[str],
        extract_depth: str = "basic",
        format: str = "markdown"
    ) -> Dict:
        """
        Extract content from URLs using Tavily Extract API.
        
        Args:
            urls: List of URLs to extract content from
            extract_depth: "basic" or "advanced"
            format: "markdown" or "html"
        
        Returns:
            Dict with results and failed_results
        """
        url = f"{self.base_url}/extract"
        
        payload = {
            "api_key": self.api_key,
            "urls": urls,
            "extract_depth": extract_depth,
            "format": format
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(url, json=payload, headers=self.headers)
                
                # Handle error status codes
                if response.status_code == 401:
                    raise Exception("Invalid Tavily API key")
                elif response.status_code == 429:
                    raise Exception("Tavily API rate limit exceeded")
                elif response.status_code == 500:
                    raise Exception("Tavily API server error")
                elif response.status_code != 200:
                    raise Exception(f"Tavily Extract API error: {response.status_code} - {response.text}")
                
                data = response.json()
                return {
                    "results": data.get("results", []),
                    "failed_results": data.get("failed_results", [])
                }
                
            except httpx.TimeoutException:
                raise Exception("Tavily extract request timed out")
            except httpx.RequestError as e:
                raise Exception(f"Tavily extract request failed: {str(e)}")
import httpx
from typing import List, Dict, Any, Optional
from app.config import settings


class TavilyClient:
    """Client for Tavily API - Web search and content extraction"""
    
    def __init__(self):
        self.base_url = settings.TAVILY_BASE_URL
        self.api_key = settings.TAVILY_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def search(
        self,
        query: str,
        max_results: int = 5,
        search_depth: str = "advanced",
        include_domains: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute a web search using Tavily Search API.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return (0-20)
            search_depth: "basic" (1 credit) or "advanced" (2 credits)
            include_domains: List of domains to include (e.g., [".se"])
            
        Returns:
            List of search results with url, title, content
            
        Example:
            results = await tavily_client.search(
                query="idrottsföreningar Stockholm ungdom",
                max_results=5,
                search_depth="advanced",
                include_domains=[".se"]
            )
        """
        endpoint = f"{self.base_url}/search"
        
        payload = {
            "query": query,
            "max_results": max_results,
            "search_depth": search_depth
        }
        
        if include_domains:
            payload["include_domains"] = include_domains
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    endpoint,
                    headers=self.headers,
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get('results', [])
                elif response.status_code == 401:
                    raise Exception("Tavily API authentication failed. Check your API key.")
                elif response.status_code == 429:
                    raise Exception("Tavily API rate limit exceeded.")
                else:
                    raise Exception(f"Tavily search failed: {response.status_code} - {response.text}")
                    
        except httpx.TimeoutException:
            raise Exception("Tavily search request timed out")
        except Exception as e:
            raise Exception(f"Tavily search error: {str(e)}")
    
    async def extract(
        self,
        urls: str | List[str],
        extract_depth: str = "basic",
        format: str = "markdown",
        timeout: int = 10
    ) -> Dict[str, Any]:
        """
        Extract content from one or more URLs using Tavily Extract API.
        
        Args:
            urls: Single URL string or list of URLs
            extract_depth: "basic" (1 credit/5 URLs) or "advanced" (2 credits/5 URLs)
            format: "markdown" or "text"
            timeout: Request timeout in seconds (1-60)
            
        Returns:
            Dictionary with 'results' (successful) and 'failed_results' arrays
            
        Example:
            result = await tavily_client.extract(
                urls="https://rinkebyif.se",
                extract_depth="basic",
                format="markdown"
            )
            content = result['results'][0]['raw_content']
        """
        endpoint = f"{self.base_url}/extract"
        
        payload = {
            "urls": urls,
            "extract_depth": extract_depth,
            "format": format,
            "timeout": timeout
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    endpoint,
                    headers=self.headers,
                    json=payload,
                    timeout=float(timeout + 5)  # Add buffer to HTTP timeout
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    raise Exception("Tavily API authentication failed. Check your API key.")
                elif response.status_code == 429:
                    raise Exception("Tavily API rate limit exceeded.")
                else:
                    raise Exception(f"Tavily extract failed: {response.status_code} - {response.text}")
                    
        except httpx.TimeoutException:
            raise Exception("Tavily extract request timed out")
        except Exception as e:
            raise Exception(f"Tavily extract error: {str(e)}")
    
    async def crawl(
        self,
        url: str,
        instructions: str,
        max_depth: int = 2,
        max_breadth: int = 10,
        limit: int = 15,
        extract_depth: str = "advanced",
        format: str = "markdown"
    ) -> Dict[str, Any]:
        """
        Crawl a website with AI-guided instructions using Tavily Crawl API.
        
        This method crawls multiple pages of a website (homepage, contact page,
        events page, etc.) and extracts relevant content based on instructions.
        
        Args:
            url: Starting URL to crawl
            instructions: Natural language instructions for what to extract
            max_depth: How deep to crawl (1-3, default 2)
            max_breadth: Max pages to check per level (1-20, default 10)
            limit: Total number of pages to process (1-50, default 15)
            extract_depth: "basic" or "advanced" content extraction
            format: "markdown" or "text"
            
        Returns:
            Dictionary with 'results' (successful pages) and 'failed_results' arrays
            Each result contains: url, raw_content, and other metadata
            
        Cost:
            ~3 credits per crawl (2 for advanced extract + 1 for mapping with instructions)
            
        Example:
            result = await tavily_client.crawl(
                url="https://rinkebyif.se",
                instructions=\"\"\"
                Find organization name, contact email/phone, 
                location in Stockholm, and youth events (ages 7-19).
                Check contact page, about page, and events page.
                \"\"\",
                max_depth=2,
                max_breadth=10,
                limit=15
            )
            
            # Combine content from all pages
            for page in result['results']:
                print(f"Page: {page['url']}")
                print(f"Content: {page['raw_content']}")
        """
        endpoint = f"{self.base_url}/crawl"
        
        payload = {
            "url": url,
            "instructions": instructions,
            "max_depth": max_depth,
            "max_breadth": max_breadth,
            "limit": limit,
            "extract_depth": extract_depth,
            "format": format
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    endpoint,
                    headers=self.headers,
                    json=payload,
                    timeout=90.0  # Crawling takes longer than extract
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    raise Exception("Tavily API authentication failed. Check your API key.")
                elif response.status_code == 429:
                    raise Exception("Tavily API rate limit exceeded.")
                else:
                    raise Exception(f"Tavily crawl failed: {response.status_code} - {response.text}")
                    
        except httpx.TimeoutException:
            raise Exception("Tavily crawl request timed out (90s limit)")
        except Exception as e:
            raise Exception(f"Tavily crawl error: {str(e)}")


# Create global client instance
tavily_client = TavilyClient()
