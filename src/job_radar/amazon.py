import httpx
import re
from typing import List, Any
from job_radar.models import Job
from job_radar.logger import logger

class AmazonClient:
    def get_jobs(self) -> List[dict[str, Any]]:
        """Fetch all software development jobs in India from Amazon's JSON API."""
        base_url = "https://www.amazon.jobs/en/search.json"
        
        # We query for Software Development in India, sorted by recent.
        # To avoid massive scraping overhead on every cycle, we fetch the first 500 recent jobs.
        params = {
            "category[]": "software-development",
            "country[]": "IND",
            "sort": "recent",
            "offset": 0,
            "result_limit": 100
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
        }
        
        all_jobs = []
        
        logger.info("Downloading Amazon jobs via JSON API...")
        
        with httpx.Client(headers=headers, timeout=15) as client:
            while params["offset"] < 500:
                try:
                    response = client.get(base_url, params=params)
                    response.raise_for_status()
                except httpx.HTTPStatusError as e:
                    logger.error(f"Amazon HTTP Error ({e.response.status_code}): {e.response.text}")
                    break
                except Exception as e:
                    logger.error(f"Amazon Request Error: {e}")
                    break
                    
                data = response.json()
                jobs = data.get("jobs", [])
                
                if not jobs:
                    break
                    
                all_jobs.extend(jobs)
                
                if len(jobs) < params["result_limit"]:
                    break
                    
                params["offset"] += params["result_limit"]
                
        return all_jobs

    def check_wow_program(self) -> Job | None:
        """Monitor Amazon WoW page for application links."""
        url = "https://www.amazon.jobs/content/en/career-programs/university/women-of-the-world"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        try:
            with httpx.Client(headers=headers, timeout=15) as client:
                response = client.get(url)
                response.raise_for_status()
                
                # Check for Apply/Register buttons that aren't webinar links
                html = response.text
                
                # Rough heuristic: Look for an anchor tag containing "Apply" or "Register" (case-insensitive)
                # that has an href.
                matches = re.findall(r'<a[^>]+href="([^"]+)"[^>]*>([^<]*(?:Apply|Register)[^<]*)</a>', html, re.IGNORECASE)
                
                for href, text in matches:
                    if "gotowebinar" not in href.lower() and "recording" not in href.lower():
                        # We found a plausible registration link!
                        apply_url = href
                        if apply_url.startswith("/"):
                            apply_url = "https://www.amazon.jobs" + apply_url
                            
                        return Job(
                            company="Amazon",
                            role="Amazon WoW Program",
                            location="India",
                            apply_url=apply_url,
                            source="Amazon WoW"
                        )
                        
        except Exception as e:
            logger.error(f"Amazon WoW Monitor Error: {e}")
            
        return None

def parse_amazon_jobs(raw_jobs: List[dict[str, Any]]) -> List[Job]:
    """Parse raw Amazon JSON job listings into normalized Job objects."""
    logger.info(f"Parsing {len(raw_jobs)} raw jobs from Amazon...")
    jobs = []
    
    for raw in raw_jobs:
        if not isinstance(raw, dict):
            continue
            
        title = str(raw.get("title") or "")
        location = str(raw.get("location") or "")
        job_path = str(raw.get("job_path") or "")
        
        if not job_path.startswith("/"):
            job_path = "/" + job_path
            
        apply_url = f"https://www.amazon.jobs{job_path}"
        
        job = Job(
            company="Amazon",
            role=title,
            location=location,
            apply_url=apply_url,
            source="Amazon"
        )
        jobs.append(job)
        
    return jobs
