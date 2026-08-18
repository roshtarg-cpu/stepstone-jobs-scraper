"""Utility functions for Stepstone scraper."""
import httpx
from urllib.parse import urlparse


async def _fetch(url, proxy_url=None):
    """Fetch a page using httpx with headers and optional proxy."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    proxies = None
    if proxy_url:
        proxies = {
            'http://': proxy_url,
            'https://': proxy_url
        }
    
    async with httpx.AsyncClient(
        headers=headers,
        proxies=proxies,
        timeout=30.0,
        follow_redirects=True
    ) as client:
        try:
            response = await client.get(url)
            
            # Check for valid response
            if response.status_code != 200:
                print(f"HTTP {response.status_code} for {url}")
                return None
            
            if len(response.text) < 500:
                print(f"Response too small ({len(response.text)} bytes)")
                return None
            
            return response.text
            
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
