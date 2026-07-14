import time
from job_radar.github_client import GitHubClient
from job_radar.greenhouse import GreenhouseClient, parse_greenhouse_jobs
from job_radar.workday import WorkdayClient, parse_workday_jobs
from job_radar.parser import parse_simplify_jobs
from job_radar.database import save_jobs
from job_radar.notifier import send_job
from job_radar.config import COMPANIES
from job_radar.filters import is_target_role, is_in_india, normalize_location
from job_radar.logger import logger
from job_radar.page_monitor import check_pages
import httpx


def check_companies(client, gh_client, wd_client):
    all_jobs = []
    
    companies_checked = len(COMPANIES)
    companies_succeeded = 0
    companies_failed = 0
    jobs_downloaded = 0
    
    for company in COMPANIES:
        source = company.get("source")
        name = company.get("name")
        
        try:
            if source == "greenhouse":
                board = company.get("board")
                raw_jobs = gh_client.get_jobs(board)
                jobs_downloaded += len(raw_jobs)
                parsed = parse_greenhouse_jobs(raw_jobs, name)
                all_jobs.extend(parsed)
                companies_succeeded += 1
                
            elif source == "github":
                owner = company.get("owner")
                repo = company.get("repo")
                branch = company.get("branch")
                path = company.get("path")
                
                raw_jobs = client.get_json_file(
                    owner=owner,
                    repo=repo,
                    path=path,
                    branch=branch
                )
                jobs_downloaded += len(raw_jobs)
                parsed = parse_simplify_jobs(raw_jobs, name)
                all_jobs.extend(parsed)
                companies_succeeded += 1
                
            elif source == "workday":
                careers_url = company.get("careers_url")
                raw_jobs, base_url = wd_client.get_jobs(careers_url)
                if raw_jobs:
                    jobs_downloaded += len(raw_jobs)
                    parsed = parse_workday_jobs(raw_jobs, name, base_url)
                    all_jobs.extend(parsed)
                companies_succeeded += 1
                
            elif source in ("lever", "ashby", "custom"):
                logger.info(f"Skipping {name}: '{source}' integration not implemented yet.")
                companies_succeeded += 1
                
            else:
                logger.warning(f"Unknown source type '{source}' for company {name}")
                companies_failed += 1
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP Error ({e.response.status_code}) for {name} ({source}): {e.response.text}")
            companies_failed += 1
        except Exception as e:
            logger.error(f"Unexpected Error for {name} ({source}): {e}")
            companies_failed += 1

    if not all_jobs:
        logger.warning("No jobs parsed from any company.")
        return

    india_jobs = []
    for job in all_jobs:
        if is_in_india(job):
            india_jobs.append(job)
            
    valid_jobs = []
    for job in india_jobs:
        if is_target_role(job):
            valid_jobs.append(job)

    try:
        new_jobs = save_jobs(valid_jobs)
        duplicates = len(valid_jobs) - len(new_jobs)
        
        notifications_sent = 0
        for job in new_jobs:
            logger.info(f"MATCH: {job.company} - {job.role} ({job.location})")
            send_job(job)
            notifications_sent += 1
                
        summary = (
            f"\nCompanies Checked: {companies_checked}\n"
            f"Companies Succeeded: {companies_succeeded}\n"
            f"Companies Failed: {companies_failed}\n\n"
            f"Jobs Downloaded: {jobs_downloaded}\n"
            f"Jobs Matching India: {len(india_jobs)}\n"
            f"Jobs Matching Keywords: {len(valid_jobs)}\n"
            f"Jobs Stored: {len(new_jobs)}\n"
            f"Duplicates: {duplicates}\n"
            f"Notifications Sent: {notifications_sent}\n"
        )
        logger.info(f"Cycle Summary:{summary}")

    except Exception as e:
        logger.error(f"Unexpected Error during parsing/saving: {e}")

from job_radar.amazon import AmazonClient, parse_amazon_jobs
from job_radar.config import AMAZON_CONFIG

def check_amazon(amz_client):
    if not AMAZON_CONFIG.get("enabled"):
        return
        
    all_jobs = []
    
    try:
        raw_jobs = amz_client.get_jobs()
        parsed = parse_amazon_jobs(raw_jobs)
        all_jobs.extend(parsed)
        
        wow_job = amz_client.check_wow_program()
        if wow_job:
            all_jobs.append(wow_job)
            
    except Exception as e:
        logger.error(f"Amazon Fetch Error: {e}")
        return

    if not all_jobs:
        logger.warning("No jobs parsed from Amazon.")
        return

    india_jobs = []
    for job in all_jobs:
        if is_in_india(job):
            india_jobs.append(job)
            
    valid_jobs = []
    for job in india_jobs:
        if is_target_role(job):
            valid_jobs.append(job)

    try:
        new_jobs = save_jobs(valid_jobs)
        duplicates = len(valid_jobs) - len(new_jobs)
        
        notifications_sent = 0
        for job in new_jobs:
            logger.info(f"MATCH: {job.company} - {job.role} ({job.location})")
            send_job(job)
            notifications_sent += 1
                
        summary = (
            f"\nAmazon Jobs Downloaded: {len(all_jobs)}\n"
            f"Jobs Matching India: {len(india_jobs)}\n"
            f"Jobs Matching Keywords: {len(valid_jobs)}\n"
            f"Jobs Stored: {len(new_jobs)}\n"
            f"Duplicates: {duplicates}\n"
            f"Notifications Sent: {notifications_sent}\n"
        )
        logger.info(f"Amazon Cycle Summary:{summary}")

    except Exception as e:
        logger.error(f"Unexpected Error during Amazon parsing/saving: {e}")

from job_radar.microsoft import MicrosoftClient, parse_microsoft_jobs
from job_radar.config import MICROSOFT_CONFIG

def check_microsoft(ms_client):
    if not MICROSOFT_CONFIG.get("enabled"):
        return
        
    all_jobs = []
    
    try:
        raw_jobs = ms_client.get_jobs()
        parsed = parse_microsoft_jobs(raw_jobs)
        all_jobs.extend(parsed)
            
    except Exception as e:
        logger.error(f"Microsoft Fetch Error: {e}")
        return

    if not all_jobs:
        logger.warning("No jobs parsed from Microsoft.")
        return

    india_jobs = []
    for job in all_jobs:
        if is_in_india(job):
            india_jobs.append(job)
            
    valid_jobs = []
    for job in india_jobs:
        if is_target_role(job):
            valid_jobs.append(job)

    try:
        new_jobs = save_jobs(valid_jobs)
        duplicates = len(valid_jobs) - len(new_jobs)
        
        notifications_sent = 0
        for job in new_jobs:
            logger.info(f"MATCH: {job.company} - {job.role} ({job.location})")
            send_job(job)
            notifications_sent += 1
                
        summary = (
            f"\nMicrosoft Jobs Downloaded: {len(all_jobs)}\n"
            f"Jobs Matching India: {len(india_jobs)}\n"
            f"Jobs Matching Keywords: {len(valid_jobs)}\n"
            f"Jobs Stored: {len(new_jobs)}\n"
            f"Duplicates: {duplicates}\n"
            f"Notifications Sent: {notifications_sent}\n"
        )
        logger.info(f"Microsoft Cycle Summary:{summary}")

    except Exception as e:
        logger.error(f"Unexpected Error during Microsoft parsing/saving: {e}")

def main():
    client = GitHubClient()
    gh_client = GreenhouseClient()
    wd_client = WorkdayClient()
    amz_client = AmazonClient()
    ms_client = MicrosoftClient()
    
    logger.info("Starting Job Radar daemon...")
    
    while True:
        logger.info("Initiating Companies check cycle...")
        try:
            check_companies(client, gh_client, wd_client)
        except Exception as e:
            logger.error(f"Critical Error during Companies cycle: {e}")
            
        logger.info("Initiating Amazon check cycle...")
        try:
            check_amazon(amz_client)
        except Exception as e:
            logger.error(f"Critical Error during Amazon cycle: {e}")
            
        logger.info("Initiating Microsoft check cycle...")
        try:
            check_microsoft(ms_client)
        except Exception as e:
            logger.error(f"Critical Error during Microsoft cycle: {e}")
            
        logger.info("Initiating Pages check cycle...")
        try:
            check_pages()
        except Exception as e:
            logger.error(f"Critical Error during Pages cycle: {e}")
            
        logger.info("Cycle complete. Sleeping for 5 minutes...")
        time.sleep(300)

if __name__ == "__main__":
    main()