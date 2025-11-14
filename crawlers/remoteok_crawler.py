# crawlers/remoteok_crawler.py
import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict, Any

BASE_URL = "https://remoteok.io/"

def scrape() -> List[Dict[str, Any]]:
    """
    Scrapes job postings from remoteok.io.
    """
    print("Scraping remoteok.io...")
    jobs = []
    try:
        response = requests.get(BASE_URL, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        job_rows = soup.find_all('tr', class_='job')
        
        for job_row in job_rows:
            if 'data-url' not in job_row.attrs:
                continue

            job_url_path = job_row['data-url']
            full_url = f"{BASE_URL}{job_url_path}"
            
            title_element = job_row.find('h2', itemprop='title')
            company_element = job_row.find('h3', itemprop='name')
            time_element = job_row.find('time')
            
            title = title_element.text.strip() if title_element else "N/A"
            company = company_element.text.strip() if company_element else "N/A"
            
            # Extract tags
            tags = [tag.text.strip() for tag in job_row.find_all('div', class_='tag')]
            
            # The description is often in a separate div within the row
            description_element = job_row.find('div', class_='description')
            description = description_element.text.strip().replace('\n', ' ').replace('\r', ' ') if description_element else ""

            job_data = {
                "url": full_url,
                "title": title,
                "company": company,
                "tags": tags,
                "description": description,
                "source": "remoteok",
                "posted_at": time_element['datetime'] if time_element and 'datetime' in time_element.attrs else time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            }
            jobs.append(job_data)
            
        print(f"Found {len(jobs)} jobs from remoteok.io")
        return jobs

    except requests.RequestException as e:
        print(f"Error scraping remoteok.io: {e}")
        return []

if __name__ == '__main__':
    # For direct testing of the crawler
    scraped_jobs = scrape()
    if scraped_jobs:
        print(f"Successfully scraped {len(scraped_jobs)} jobs.")
        # print(scraped_jobs[0])
