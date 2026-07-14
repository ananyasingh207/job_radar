from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_API = os.getenv("GITHUB_API")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")