import httpx
import re
from typing import List, Any
from job_radar.models import Job
from job_radar.logger import logger

class WorkdayClient:
    def get_jobs(self, careers_url: str) -> List[dict[str, Any]]:
        """Download jobs for a given Workday careers URL using the internal CXS JSON API."""
        # Extract the base URL, tenant, and site from the careers_url
        # Example: https://flipkart.wd3.myworkdayjobs.com/Flipkart
        match = re.match(r'(https://([a-zA-Z0-9\-]+)\.[a-zA-Z0-9\-]+\.myworkdayjobs\.com)/([a-zA-Z0-9\-_]+)', careers_url)
        if not match:
            logger.error(f"Could not parse Workday URL: {careers_url}")
            return []
            
        base_url = match.group(1)
        tenant = match.group(2)
        site = match.group(3)
        
        api_url = f"{base_url}/wday/cxs/{tenant}/{site}/jobs"
        logger.info(f"Downloading Workday jobs from {api_url}...")
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        all_jobs = []
        offset = 0
        limit = 20
        
        with httpx.Client(headers=headers, timeout=15) as client:
            while True:
                payload = {
                    "appliedFacets": {},
                    "limit": limit,
                    "offset": offset,
                    "searchText": ""
                }
                
                try:
                    response = client.post(api_url, json=payload)
                    response.raise_for_status()
                except httpx.HTTPStatusError as e:
                    logger.error(f"Workday HTTP Error ({e.response.status_code}) for {careers_url}: {e.response.text}")
                    break
                except Exception as e:
                    logger.error(f"Workday Request Error for {careers_url}: {e}")
                    break
                    
                data = response.json()
                job_postings = data.get("jobPostings", [])
                
                if not job_postings:
                    break
                    
                all_jobs.extend(job_postings)
                
                if len(job_postings) < limit:
                    break
                    
                offset += limit
                
        return all_jobs, base_url

def parse_workday_jobs(raw_jobs: List[dict[str, Any]], company_name: str, base_url: str) -> List[Job]:
    """Parse raw Workday JSON job listings into normalized Job objects."""
    logger.info(f"Parsing {len(raw_jobs)} raw jobs from Workday ({company_name})...")
    jobs = []
    
    for raw in raw_jobs:
        if not isinstance(raw, dict):
            continue
            
        location = str(raw.get("locationsText") or "")
        title = str(raw.get("title") or "")
        external_path = str(raw.get("externalPath") or "")
        
        # Workday URLs are usually base_url/en-US{externalPath} or base_url{externalPath}
        # Let's construct a reliable absolute URL
        if not external_path.startswith("/"):
            external_path = "/" + external_path
            
        apply_url = f"{base_url}{external_path}"
        
        job = Job(
            company=company_name,
            role=title,
            location=location,
            apply_url=apply_url,
            source="Workday"
        )
        jobs.append(job)
        
    return jobs
