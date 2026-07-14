from job_radar.config import KEYWORDS
from job_radar.models import Job

def should_notify(job: Job) -> bool:
    """
    Check if a job matches any of the notification keywords.
    Matching is done on the job role in a case-insensitive manner.
    """
    role_lower = job.role.lower()
    for keyword in KEYWORDS:
        if keyword.lower() in role_lower:
            return True
    return False
