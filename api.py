# api.py
from fastapi import FastAPI
from database import get_jobs

app = FastAPI(
    title="Remote Job API",
    description="An API to serve remote job listings scraped from various sources.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Remote Job API. Go to /jobs to see the listings."}

@app.get("/jobs")
def list_jobs():
    """
    Endpoint to get all job listings from the database.
    """
    jobs = get_jobs()
    return {"count": len(jobs), "jobs": jobs}

# To run this API:
# uvicorn api:app --reload
