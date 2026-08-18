"""Parser functions for extracting job data from Stepstone pages."""
import re
import json
from bs4 import BeautifulSoup


def _extract_next_data(html):
    """Try to extract __NEXT_DATA__ JSON from page."""
    try:
        soup = BeautifulSoup(html, 'lxml')
        script = soup.find('script', id='__NEXT_DATA__', type='application/json')
        if script and script.string:
            data = json.loads(script.string)
            return data
    except Exception as e:
        print(f"Could not extract __NEXT_DATA__: {e}")
    return None


def parse_job_listing(html, url):
    """Parse a single job listing from HTML."""
    next_data = _extract_next_data(html)
    
    # Try to extract from Next.js data first
    if next_data:
        try:
            # Navigate the Next.js data structure
            props = next_data.get('props', {}).get('pageProps', {})
            job = props.get('job', {})
            
            if job:
                return {
                    'title': job.get('title'),
                    'company': job.get('company', {}).get('name'),
                    'location': job.get('location', {}).get('label'),
                    'salary': job.get('salary', {}).get('label'),
                    'employmentType': job.get('employmentType'),
                    'url': url,
                    'scrapedAt': None  # Will be set in main
                }
        except Exception as e:
            print(f"Error parsing Next.js data: {e}")
    
    # Fallback to HTML parsing
    soup = BeautifulSoup(html, 'lxml')
    
    # Extract job details from HTML structure
    title = None
    company = None
    location = None
    salary = None
    
    # Try common selectors
    title_elem = soup.select_one('h1[data-at="job-title"], h1.job-title, h1')
    if title_elem:
        title = title_elem.get_text(strip=True)
    
    company_elem = soup.select_one('[data-at="company-name"], .company-name')
    if company_elem:
        company = company_elem.get_text(strip=True)
    
    location_elem = soup.select_one('[data-at="job-location"], .job-location')
    if location_elem:
        location = location_elem.get_text(strip=True)
    
    return {
        'title': title,
        'company': company,
        'location': location,
        'salary': salary,
        'employmentType': None,
        'url': url,
        'scrapedAt': None
    }


def parse_search_results(html):
    """Parse job listings from search results page."""
    jobs = []
    next_data = _extract_next_data(html)
    
    if next_data:
        try:
            # Extract search results from Next.js data
            props = next_data.get('props', {}).get('pageProps', {})
            listings = props.get('searchResults', {}).get('results', [])
            
            for listing in listings:
                job_url = listing.get('url', '')
                if job_url and not job_url.startswith('http'):
                    job_url = f"https://www.stepstone.de{job_url}"
                
                jobs.append({
                    'title': listing.get('title') or '',
                    'company': listing.get('company', {}).get('name') or '',
                    'location': listing.get('location', {}).get('label') or '',
                    'salary': listing.get('salary', {}).get('label') or '',
                    'employmentType': listing.get('employmentType') or '',
                    'url': job_url,
                    'scrapedAt': ''
                })
        except Exception as e:
            print(f"Error parsing search results from Next.js: {e}")
    
    # Fallback: parse HTML
    if not jobs:
        soup = BeautifulSoup(html, 'lxml')
        job_cards = soup.select('article[data-at="job-item"], .job-element, li.res-list__item')
        
        for card in job_cards[:20]:  # Limit to first 20
            title_elem = card.select_one('[data-at="job-item-title"], h3 a, .job-element__title a')
            if not title_elem:
                continue
            
            job_url = title_elem.get('href', '')
            if job_url and not job_url.startswith('http'):
                job_url = f"https://www.stepstone.de{job_url}"
            
            company_elem = card.select_one('[data-at="job-item-company-name"], .job-element__company')
            location_elem = card.select_one('[data-at="job-item-location"], .job-element__location')
            
            jobs.append({
                'title': title_elem.get_text(strip=True),
                'company': company_elem.get_text(strip=True) if company_elem else '',
                'location': location_elem.get_text(strip=True) if location_elem else '',
                'salary': '',
                'employmentType': '',
                'url': job_url,
                'scrapedAt': ''
            })
    
    return jobs
