import sqlite3
import hashlib
from pathlib import Path
from typing import List
from job_radar.models import Job
from job_radar.logger import logger

DB_PATH = Path(__file__).parent.parent.parent / "data" / "jobs.db"

def _get_job_hash(job: Job) -> str:
    """Generate a unique hash for a job."""
    unique_string = f"{job.company}|{job.role}|{job.location}|{job.apply_url}|{job.source}"
    return hashlib.sha256(unique_string.encode('utf-8')).hexdigest()

def init_db():
    """Initialize the database and create the jobs table if it doesn't exist."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                hash TEXT PRIMARY KEY,
                company TEXT,
                role TEXT,
                location TEXT,
                apply_url TEXT,
                source TEXT
            )
        """)
        conn.commit()

def save_jobs(jobs: List[Job]) -> List[Job]:
    """
    Save jobs to the database, ignoring duplicates.
    Returns a list of newly inserted Job objects.
    """
    logger.info(f"Checking {len(jobs)} parsed jobs against the database...")
    init_db()
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT hash FROM jobs")
        existing_hashes = {row[0] for row in cursor.fetchall()}
        
        new_jobs = []
        data = []
        for job in jobs:
            job_hash = _get_job_hash(job)
            if job_hash not in existing_hashes:
                new_jobs.append(job)
                data.append((job_hash, job.company, job.role, job.location, job.apply_url, job.source))
                existing_hashes.add(job_hash)
                
        if data:
            cursor.executemany("""
                INSERT INTO jobs (hash, company, role, location, apply_url, source)
                VALUES (?, ?, ?, ?, ?, ?)
            """, data)
            conn.commit()
            
    logger.info(f"Stored {len(new_jobs)} new jobs. Skipped {len(jobs) - len(new_jobs)} existing.")
    return new_jobs

def get_all_jobs() -> List[Job]:
    """Retrieve all jobs from the database."""
    init_db()
    
    jobs = []
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT company, role, location, apply_url, source FROM jobs")
        for row in cursor.fetchall():
            jobs.append(Job(
                company=row[0],
                role=row[1],
                location=row[2],
                apply_url=row[3],
                source=row[4]
            ))
            
    return jobs
