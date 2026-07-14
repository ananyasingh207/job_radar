import httpx
from typing import List, Any
from job_radar.models import Job
from job_radar.logger import logger

class MicrosoftClient:
    def get_jobs(self) -> List[dict[str, Any]]:
        """Fetch software jobs in India from Microsoft's internal API."""
        base_url = "https://apply.careers.microsoft.com/api/pcsx/search"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
        }
        
        all_jobs = []
        start = 0
        limit = 500 # max jobs to fetch to avoid over-scraping
        
        logger.info("Downloading Microsoft jobs via JSON API...")
        
        with httpx.Client(headers=headers, timeout=15) as client:
            while start < limit:
                params = {
                    "domain": "microsoft.com",
                    "query": "software",
                    "location": "India",
                    "start": start
                }
                
                try:
                    response = client.get(base_url, params=params)
                    response.raise_for_status()
                except httpx.HTTPStatusError as e:
                    logger.error(f"Microsoft HTTP Error ({e.response.status_code}): {e.response.text}")
                    break
                except Exception as e:
                    logger.error(f"Microsoft Request Error: {e}")
                    break
                    
                data = response.json().get("data", {})
                positions = data.get("positions", [])
                
                if not positions:
                    break
                    
                all_jobs.extend(positions)
                start += len(positions)
                
        return all_jobs

def parse_microsoft_jobs(raw_jobs: List[dict[str, Any]]) -> List[Job]:
    """Parse raw Microsoft JSON job listings into normalized Job objects."""
    logger.info(f"Parsing {len(raw_jobs)} raw jobs from Microsoft...")
    jobs = []
    
    for raw in raw_jobs:
        if not isinstance(raw, dict):
            continue
            
        title = str(raw.get("name") or "")
        
        # locations is a list like ["India, Telangana, Hyderabad"]
        locations_list = raw.get("locations", [])
        location = ", ".join(locations_list) if locations_list else ""
        
        job_id = raw.get("displayJobId")
        if not job_id:
            continue
            
        apply_url = f"https://jobs.careers.microsoft.com/global/en/job/{job_id}"
        
        job = Job(
            company="Microsoft",
            role=title,
            location=location,
            apply_url=apply_url,
            source="Microsoft"
        )
        jobs.append(job)
        
    return jobs
