from typing import Any
from job_radar.models import Job
from job_radar.logger import logger

def parse_simplify_jobs(raw_jobs: list[dict[str, Any]], repo_name: str) -> list[Job]:
    """
    Parse raw JSON job listings from SimplifyJobs into normalized Job objects.
    
    Args:
        raw_jobs: List of dictionaries representing job listings.
        repo_name: Name of the repository the jobs came from.
        
    Returns:
        List of normalized Job dataclass objects.
    """
    logger.info(f"Parsing {len(raw_jobs)} raw jobs from {repo_name}...")
    jobs = []
    for raw_job in raw_jobs:
        if not isinstance(raw_job, dict):
            continue
            
        locations = raw_job.get("locations")
        if isinstance(locations, list):
            location = ", ".join(str(loc) for loc in locations if loc)
        elif locations:
            location = str(locations)
        else:
            location = ""
            
        job = Job(
            company=str(raw_job.get("company_name") or ""),
            role=str(raw_job.get("title") or ""),
            location=location,
            apply_url=str(raw_job.get("url") or ""),
            source=repo_name
        )
        jobs.append(job)
        
    return jobs
