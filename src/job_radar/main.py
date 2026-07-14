import time
from job_radar.github_client import GitHubClient
from job_radar.parser import parse_simplify_jobs
from job_radar.database import save_jobs
from job_radar.notifier import send_job
from job_radar.config import REPOSITORIES
from job_radar.filters import is_target_role, is_in_india, normalize_location
from job_radar.logger import logger
import httpx


def check_repositories(client):
    all_jobs = []
    
    repos_checked = len(REPOSITORIES)
    repos_succeeded = 0
    repos_failed = 0
    jobs_downloaded = 0
    
    for repo_conf in REPOSITORIES:
        name = repo_conf["name"]
        owner = repo_conf["owner"]
        repo = repo_conf["repo"]
        branch = repo_conf["branch"]
        path = repo_conf["path"]
        
        try:
            raw_jobs = client.get_json_file(
                owner=owner,
                repo=repo,
                path=path,
                branch=branch
            )
            jobs_downloaded += len(raw_jobs)
            parsed = parse_simplify_jobs(raw_jobs, name)
            all_jobs.extend(parsed)
            repos_succeeded += 1
        except httpx.HTTPStatusError as e:
            logger.error(f"GitHub Error ({e.response.status_code}) for {owner}/{repo}: {e.response.text}")
            repos_failed += 1
        except Exception as e:
            logger.error(f"Unexpected Error for {owner}/{repo}: {e}")
            repos_failed += 1

    if not all_jobs:
        logger.warning("No jobs parsed from any repository.")
        return

    valid_jobs = []
    jobs_skipped_location = 0
    jobs_skipped_role = 0
    
    for job in all_jobs:
        if not is_in_india(job):
            norm_loc = normalize_location(job.location)
            logger.info(
                f"Skipped: {job.company} - {job.role}\n"
                f"Original Location: {job.location}\n"
                f"Normalized Location: {norm_loc}\n"
                f"Reason: Outside allowed locations"
            )
            jobs_skipped_location += 1
            continue
            
        if not is_target_role(job):
            logger.info(f"Skipped: {job.company} - {job.role}\nReason: Role does not match software engineering keywords")
            jobs_skipped_role += 1
            continue
            
        valid_jobs.append(job)

    try:
        new_jobs = save_jobs(valid_jobs)
        duplicates = len(valid_jobs) - len(new_jobs)
        
        notifications_sent = 0
        jobs_matching_india = len(all_jobs) - jobs_skipped_location
        jobs_matching_keywords = len(valid_jobs)
        
        for job in new_jobs:
            logger.info(f"MATCH: {job.company} - {job.role} ({job.location})")
            send_job(job)
            notifications_sent += 1
                
        summary = (
            f"\nJobs Downloaded: {jobs_downloaded}\n"
            f"Jobs Matching India: {jobs_matching_india}\n"
            f"Jobs Matching Keywords: {jobs_matching_keywords}\n"
            f"Jobs Stored: {len(new_jobs)}\n"
            f"Duplicates: {duplicates}\n"
            f"Notifications Sent: {notifications_sent}\n"
            f"Jobs Skipped (Outside India): {jobs_skipped_location}\n"
            f"Jobs Skipped (Role Mismatch): {jobs_skipped_role}\n"
        )
        logger.info(f"Cycle Summary:{summary}")

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