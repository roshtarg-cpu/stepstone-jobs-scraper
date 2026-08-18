"""Utility functions for Stepstone scraper."""
import re
from urllib.parse import urlparse, parse_qs
from camoufox.async_api import AsyncCamoufox


def _parse_proxy(proxy_url):
    """Parse Apify proxy URL into components."""
    if not proxy_url:
        return None
    
    parsed = urlparse(proxy_url)
    return {
        'server': f'{parsed.scheme}://{parsed.hostname}:{parsed.port}',
        'username': parsed.username,
        'password': parsed.password
    }


async def _fetch(url, proxy_url=None):
    """Fetch a page using Camoufox with optional proxy."""
    proxy_config = _parse_proxy(proxy_url) if proxy_url else None
    
    async with AsyncCamoufox(
        headless=True,
        geoip=True,
        proxy=proxy_config
    ) as browser:
        page = await browser.new_page()
        
        try:
            response = await page.goto(
                url,
                wait_until='networkidle',
                timeout=90000
            )
            
            # Wait for content to load
            await page.wait_for_timeout(3000)
            
            html = await page.content()
            
            # Check for valid response
            if len(html) < 500:
                return None
                
            return html
            
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
        finally:
            await page.close()
