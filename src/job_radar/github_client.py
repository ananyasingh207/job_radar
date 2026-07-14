import httpx

from job_radar.config import GITHUB_API, GITHUB_TOKEN


class GitHubClient:
    def __init__(self):
        self.base_url = GITHUB_API

        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def get_repository(self, owner: str, repo: str):
        url = f"{self.base_url}/repos/{owner}/{repo}"

        response = httpx.get(
            url,
            headers=self.headers,
            timeout=10,
        )

        response.raise_for_status()

        return response.json()

    def get_readme(self, owner: str, repo: str):
        url = f"{self.base_url}/repos/{owner}/{repo}/readme"

        response = httpx.get(
            url,
            headers=self.headers,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        download_url = data["download_url"]

        response = httpx.get(download_url, timeout=10)

        response.raise_for_status()

        return response.text
    
    def get_json_file(self, owner: str, repo: str, path: str, branch: str = "dev"):
        from job_radar.logger import logger
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
        logger.info(f"Downloading JSON from {owner}/{repo}")

        response = httpx.get(url, timeout=20)

        response.raise_for_status()

        return response.json()