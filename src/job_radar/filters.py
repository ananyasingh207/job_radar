import re
from job_radar.config import ROLE_KEYWORDS, EXCLUDED_KEYWORDS, ALLOWED_LOCATIONS
from job_radar.models import Job

def normalize_title(title: str) -> str:
    """Normalize a job title before matching."""
    t = title.lower()
    t = re.sub(r'[,\-/\(\)]', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def is_target_role(job: Job) -> bool:
    """
    Check if a job matches any of the engineering role keywords
    and does not match any excluded non-engineering keywords.
    Matching is done on the normalized job role in a case-insensitive manner.
    """
    role_norm = normalize_title(job.role)
    
    for kw in EXCLUDED_KEYWORDS:
        if kw in role_norm:
            return False
            
    for keyword in ROLE_KEYWORDS:
        if keyword.lower() in role_norm:
            return True
            
    return False

def normalize_location(location: str) -> str:
    """
    Normalize location by lowercasing, removing punctuation, 
    and standardizing spaces for robust matching.
    """
    loc = location.lower()
    loc = re.sub(r'[,/\-]', ' ', loc)
    loc = loc.replace('(', '').replace(')', '')
    loc = re.sub(r'\s+', ' ', loc).strip()
    return loc

def is_in_india(job: Job) -> bool:
    """
    Check if a job's normalized location matches any normalized allowed India locations.
    """
    norm_loc = normalize_location(job.location)
    for loc in ALLOWED_LOCATIONS:
        norm_allowed = normalize_location(loc)
        if norm_allowed in norm_loc:
            return True
    return False
