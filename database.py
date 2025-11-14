# database.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise EnvironmentError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")

supabase: Client = create_client(url, key)

def save_jobs(jobs: List[Dict[str, Any]]):
    """
    Saves a list of job dictionaries to the Supabase 'jobs' table.
    It uses 'upsert' to avoid creating duplicate entries based on the 'url' field.
    """
    if not jobs:
        print("No jobs to save.")
        return
    try:
        # The 'on_conflict' parameter specifies the column that has a UNIQUE constraint.
        # When a conflict occurs on this column, the existing record will be updated.
        data, count = supabase.table('jobs').upsert(jobs, on_conflict='url').execute()
        print(f"Successfully upserted {len(data[1])} jobs.")
        return data
    except Exception as e:
        print(f"An error occurred while saving jobs to Supabase: {e}")
        return None

def get_jobs():
    """
    Retrieves all jobs from the Supabase 'jobs' table.
    """
    try:
        data, count = supabase.table('jobs').select('*').order('posted_at', desc=True).execute()
        return data[1] # The actual data is in the second element of the tuple
    except Exception as e:
        print(f"An error occurred while fetching jobs from Supabase: {e}")
        return []

