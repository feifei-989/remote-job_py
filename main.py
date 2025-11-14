# main.py
import sys
import importlib
from database import save_jobs
from config import CRAWLER_TARGETS
import uvicorn

def run_crawlers():
    """
    Dynamically imports and runs crawlers specified in the config.
    """
    print("Starting crawler process...")
    all_jobs = []
    for target in CRAWLER_TARGETS:
        try:
            crawler_module = importlib.import_module(f"crawlers.{target}_crawler")
            print(f"Running crawler for {target}...")
            jobs = crawler_module.scrape()
            if jobs:
                all_jobs.extend(jobs)
        except ImportError:
            print(f"Error: Crawler for '{target}' not found.")
        except Exception as e:
            print(f"An error occurred while running the '{target}' crawler: {e}")
    
    if all_jobs:
        print(f"Total jobs scraped: {len(all_jobs)}")
        save_jobs(all_jobs)
    else:
        print("No jobs were scraped.")

def start_api():
    """
    Starts the FastAPI server.
    """
    print("Starting API server on http://127.0.0.1:8000")
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "crawlers":
            run_crawlers()
        elif command == "api":
            start_api()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: 'crawlers', 'api'")
    else:
        print("No command specified. Running crawlers by default.")
        run_crawlers()

