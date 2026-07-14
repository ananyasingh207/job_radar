from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_API = os.getenv("GITHUB_API")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

REPOSITORIES = [
    ("SimplifyJobs", "Summer2026-Internships", ".github/scripts/listings.json", "dev")
]

KEYWORDS = [
    "intern", "software", "engineer", "sde", "backend", "frontend",
    "full stack", "front end", "back end", "developer", "development",
    "web", "new grad", "associate"
]