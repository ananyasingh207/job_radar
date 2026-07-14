from job_radar.github_client import GitHubClient
import httpx
import json


def main():
    client = GitHubClient()

    try:
        jobs = client.get_json_file(
            owner="SimplifyJobs",
            repo="Summer2026-Internships",
            path=".github/scripts/listings.json",
        )

        print(f"Total Jobs: {len(jobs)}\n")

        print(json.dumps(jobs[0], indent=4))

    except httpx.HTTPStatusError as e:
        print(f"GitHub Error ({e.response.status_code})")
        print(e.response.text)

    except Exception as e:
        print(f"Unexpected Error: {e}")


if __name__ == "__main__":
    main()