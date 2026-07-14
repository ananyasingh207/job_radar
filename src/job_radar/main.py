import time
from job_radar.github_client import GitHubClient
from job_radar.parser import parse_simplify_jobs
from job_radar.database import save_jobs
from job_radar.notifier import send_job
from job_radar.config import REPOSITORIES
from job_radar.filters import should_notify
from job_radar.logger import logger
import httpx


def check_repositories(client):
    all_raw_jobs = []
    
    for owner, repo, path, branch in REPOSITORIES:
        try:
            raw_jobs = client.get_json_file(
                owner=owner,
                repo=repo,
                path=path,
                branch=branch
            )
            all_raw_jobs.extend(raw_jobs)
        except httpx.HTTPStatusError as e:
            logger.error(f"GitHub Error ({e.response.status_code}) for {owner}/{repo}: {e.response.text}")
        except Exception as e:
            logger.error(f"Unexpected Error for {owner}/{repo}: {e}")

    if not all_raw_jobs:
        logger.warning("No raw jobs fetched from any repository.")
        return

    try:
        jobs = parse_simplify_jobs(all_raw_jobs)
        
        new_jobs = save_jobs(jobs)

        for job in new_jobs:
            if should_notify(job):
                logger.info(f"MATCH: {job.company} - {job.role} ({job.location})")
                send_job(job)

    except Exception as e:
        logger.error(f"Unexpected Error during parsing/saving: {e}")


def main():
    client = GitHubClient()
    
    logger.info("Starting Job Radar daemon...")
    
    while True:
        logger.info("Initiating repository check cycle...")
        
        try:
            check_repositories(client)
        except Exception as e:
            logger.error(f"Critical Error during cycle: {e}")
            
        logger.info("Cycle complete. Sleeping for 5 minutes...")
        time.sleep(300)


if __name__ == "__main__":
    main()