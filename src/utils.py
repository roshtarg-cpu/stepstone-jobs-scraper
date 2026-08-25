"""Utility functions for Stepstone scraper."""
import httpx
from urllib.parse import urlparse


async def _fetch(url, proxy_url=None):
    """Fetch a page using httpx with headers and optional proxy."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.stepstone.de/',
        'Connection': 'keep-alive'
    }
    
    proxies = None
    if proxy_url:
        proxies = proxy_url  # httpx expects a string or dict mapping schemes
    
    async with httpx.AsyncClient(
        headers=headers,
        proxy=proxies,  # Changed from 'proxies' to 'proxy'
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
