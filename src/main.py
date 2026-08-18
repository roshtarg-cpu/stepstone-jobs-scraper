"""Main entry point for Stepstone Jobs Scraper."""
import asyncio
from datetime import datetime, timezone
from apify import Actor
from .utils import _fetch
from .parser import parse_search_results, parse_job_listing


async def main():
    """Main scraper logic."""
    async with Actor:
        # Get input
        actor_input = await Actor.get_input() or {}
        search_query = actor_input.get('searchQuery', 'python developer')
        location = actor_input.get('location', '')
        max_results = actor_input.get('maxResults', 50)
        proxy_config = actor_input.get('proxyConfiguration')
        
        Actor.log.info(f'Starting Stepstone scraper - Query: {search_query}, Max: {max_results}')
        
        # Build proxy URL if configured
        proxy_url = None
        if proxy_config and proxy_config.get('useApifyProxy'):
            groups = proxy_config.get('apifyProxyGroups', ['RESIDENTIAL'])
            group = groups[0] if groups else 'RESIDENTIAL'
            proxy_password = Actor.get_env('APIFY_PROXY_PASSWORD')
            if proxy_password:
                proxy_url = f'http://groups-{group}:{proxy_password}@proxy.apify.com:8000'
                Actor.log.info(f'Using Apify proxy: {group}')
        
        # Build search URL
        search_url = f"https://www.stepstone.de/5/ergebnisseite.html?what={search_query.replace(' ', '+')}"
        if location:
            search_url += f"&where={location.replace(' ', '+')}"
        
        Actor.log.info(f'Search URL: {search_url}')
        
        results_scraped = 0
        page = 1
        max_retries = 3
        
        while results_scraped < max_results:
            # Paginate
            page_url = f"{search_url}&page={page}"
            
            Actor.log.info(f'Fetching page {page}: {page_url}')
            
            # Fetch with retries
            html = None
            for attempt in range(max_retries):
                try:
                    html = await _fetch(page_url, proxy_url)
                    if html:
                        break
                    Actor.log.warning(f'Empty response on attempt {attempt+1}/{max_retries}')
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                except Exception as e:
                    Actor.log.error(f'Fetch attempt {attempt+1} failed: {e}')
                    await asyncio.sleep(2 ** attempt)
            
            if not html:
                Actor.log.error(f'Failed to fetch page {page} after {max_retries} attempts')
                break
            
            # Parse search results
            jobs = parse_search_results(html)
            
            if not jobs:
                Actor.log.info('No more jobs found')
                break
            
            Actor.log.info(f'Found {len(jobs)} jobs on page {page}')
            
            # Process each job
            for job in jobs:
                if results_scraped >= max_results:
                    break
                
                # Add timestamp
                job['scrapedAt'] = datetime.now(timezone.utc).isoformat()
                
                # Push to dataset immediately
                await Actor.push_data(job)
                results_scraped += 1
                
                if results_scraped % 10 == 0:
                    Actor.log.info(f'Scraped {results_scraped}/{max_results} jobs')
            
            # Check if we should continue
            if results_scraped >= max_results:
                break
            
            # Next page
            page += 1
            
            # Safety limit
            if page > 20:
                Actor.log.warning('Reached page limit (20)')
                break
        
        Actor.log.info(f'✓ Scraping complete: {results_scraped} jobs scraped')


if __name__ == '__main__':
    asyncio.run(main())
