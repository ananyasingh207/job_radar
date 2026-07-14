from job_radar.github_client import GitHubClient
from job_radar.parser import parse_simplify_jobs
from job_radar.database import save_jobs
import httpx


def main():
    client = GitHubClient()

    try:
        raw_jobs = client.get_json_file(
            owner="SimplifyJobs",
            repo="Summer2026-Internships",
            path=".github/scripts/listings.json",
        )

        jobs = parse_simplify_jobs(raw_jobs)
        
        inserted, skipped = save_jobs(jobs)

        print(f"New jobs inserted: {inserted}")
        print(f"Existing jobs skipped: {skipped}")

    except httpx.HTTPStatusError as e:
        print(f"GitHub Error ({e.response.status_code})")
        print(e.response.text)

    except Exception as e:
        print(f"Unexpected Error: {e}")


if __name__ == "__main__":
    main()