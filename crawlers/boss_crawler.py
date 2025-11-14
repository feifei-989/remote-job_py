# crawlers/boss_crawler.py
import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict, Any

# Note: Scraping Boss Zhipin is difficult due to anti-scraping measures.
# This crawler is a best-effort attempt and may fail or require updates.
# The site often uses dynamic rendering, so a simple requests.get() may not work.

BASE_URL = "https://www.zhipin.com/web/geek/job?query=远程"

def scrape() -> List[Dict[str, Any]]:
    """
    Scrapes job postings from Boss Zhipin for remote positions.
    """
    print("Scraping Boss Zhipin...")
    jobs = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
    }

    try:
        # It's good practice to use a session object
        session = requests.Session()
        response = session.get(BASE_URL, headers=headers, timeout=15)
        response.raise_for_status()
        
        # It's possible the page requires cookies, which a session helps manage.
        # A second request might be needed after an initial cookie-setting visit.
        time.sleep(2) # Wait a bit before parsing
        response = session.get(BASE_URL, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # The class names for job listings can change. This is a guess based on inspection.
        job_list_items = soup.find_all('li', class_='job-card-wrapper')
        
        if not job_list_items:
            print("Warning: Could not find job listings. The page structure may have changed or content is loaded dynamically.")
            # print(soup.prettify()) # Uncomment for debugging the HTML content
            return []

        for item in job_list_items:
            title_element = item.find('span', class_='job-name')
            company_element = item.find('a', class_='company-name')
            url_element = item.find('a', class_='job-card-left')
            
            title = title_element.text.strip() if title_element else "N/A"
            company = company_element.text.strip() if company_element else "N/A"
            job_url = url_element['href'] if url_element and 'href' in url_element.attrs else "N/A"
            full_url = f"https://www.zhipin.com{job_url}" if job_url.startswith('/') else job_url

            tags_elements = item.find_all('li', class_='tag-item')
            tags = [tag.text.strip() for tag in tags_elements]

            job_data = {
                "url": full_url,
                "title": title,
                "company": company,
                "tags": tags,
                "description": f"Location/Experience tags: {', '.join(tags)}", # Description is not easily available on the list page
                "source": "boss",
                "posted_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()) # Boss doesn't show absolute time on list page
            }
            
            # Avoid adding incomplete entries
            if "N/A" not in [job_data['url'], job_data['title']]:
                jobs.append(job_data)

        print(f"Found {len(jobs)} jobs from Boss Zhipin")
        return jobs

    except requests.RequestException as e:
        print(f"Error scraping Boss Zhipin: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

if __name__ == '__main__':
    scraped_jobs = scrape()
    if scraped_jobs:
        print(f"Successfully scraped {len(scraped_jobs)} jobs.")
    else:
        print("Scraping failed or found no jobs.")
