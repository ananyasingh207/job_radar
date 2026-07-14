import httpx
from typing import List, Any
from job_radar.models import Job
from job_radar.logger import logger

class GreenhouseClient:
    BASE_URL = "https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
    
    def get_jobs(self, company: str) -> List[dict[str, Any]]:
        """Download jobs for a given company from Greenhouse."""
        url = self.BASE_URL.format(company=company)
        logger.info(f"Downloading Greenhouse jobs for {company}...")
        
        response = httpx.get(url, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        return data.get("jobs", [])

def parse_greenhouse_jobs(raw_jobs: List[dict[str, Any]], company_id: str) -> List[Job]:
    """Parse raw Greenhouse JSON job listings into normalized Job objects."""
    logger.info(f"Parsing {len(raw_jobs)} raw jobs from Greenhouse ({company_id})...")
    jobs = []
    
    for raw in raw_jobs:
        if not isinstance(raw, dict):
            continue
            
        location_dict = raw.get("location", {})
        location = str(location_dict.get("name") or "")
        company_name = str(raw.get("company_name") or company_id.title())
        
        job = Job(
            company=company_name,
            role=str(raw.get("title") or ""),
            location=location,
            apply_url=str(raw.get("absolute_url") or ""),
            source="Greenhouse"
        )
        jobs.append(job)
        
    return jobs
