from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_API = os.getenv("GITHUB_API")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

REPOSITORIES = [
    {
        "name": "Simplify Summer 2026",
        "owner": "SimplifyJobs",
        "repo": "Summer2026-Internships",
        "branch": "dev",
        "path": ".github/scripts/listings.json",
    },
    {
        "name": "Simplify New Grad",
        "owner": "SimplifyJobs",
        "repo": "New-Grad-Positions",
        "branch": "main",
        "path": ".github/scripts/listings.json",
    },
    {
        "name": "SpeedyApply SWE Jobs",
        "owner": "speedyapply",
        "repo": "2026-SWE-College-Jobs",
        "branch": "main",
        "path": ".github/scripts/listings.json",
    },
]

ROLE_KEYWORDS = [
    # Internship
    "intern",
    "internship",
    "summer intern",
    "winter intern",
    "software intern",
    "engineering intern",
    "swe intern",

    # New Grad / Entry Level
    "new grad",
    "new graduate",
    "graduate",
    "graduate program",
    "graduate engineer",
    "graduate software engineer",
    "entry level",
    "entry-level",
    "associate",
    "associate engineer",
    "associate software engineer",
    "junior",
    "early career",
    "campus",

    # Software Engineering
    "software",
    "software engineer",
    "software developer",
    "engineer",
    "developer",
    "development",
    "programmer",
    "coding",

    # Common Abbreviations
    "sde",
    "sde i",
    "sde 1",
    "swe",
    "se",

    # Full Stack
    "full stack",
    "fullstack",

    # Backend
    "backend",
    "back end",
    "server side",

    # Frontend
    "frontend",
    "front end",
    "ui",
    "web",

    # Languages / Technologies
    "python",
    "java",
    "c++",
    "cpp",
    "golang",
    "go",
    "rust",
    "javascript",
    "typescript",
    "react",
    "node",
    "nodejs",

    # Cloud / Infrastructure
    "cloud",
    "devops",
    "platform",
    "infrastructure",
]

EXCLUDED_KEYWORDS = [
    "marketing",
    "finance",
    "hr",
    "sales",
    "business",
    "product manager",
    "product management",
    "operations",
    "customer success",
    "recruiter",
    "talent",
    "account",
]

ALLOWED_LOCATIONS = [
    # Generic
    "india",
    "india (remote)",
    "india remote",
    "remote - india",
    "remote, india",
    "remote india",
    "india - remote",
    "india (hybrid)",
    "india - hybrid",
    "hybrid - india",
    "multiple locations, india",
    "india - multiple locations",

    # Major Tech Hubs
    "bangalore",
    "bengaluru",
    "hyderabad",
    "pune",
    "gurgaon",
    "gurugram",
    "noida",
    "new delhi",
    "delhi",
    "mumbai",
    "chennai",
    "kolkata",
    "ahmedabad",
    "kochi",
    "cochin",
    "trivandrum",
    "thiruvananthapuram",
    "jaipur",
    "indore",
    "bhubaneswar",
    "mysore",
    "mysuru",
    "nagpur",
    "lucknow",
    "vadodara",
    "surat",
    "coimbatore",
    "visakhapatnam",
    "vizag",
    "vijayawada",
    "mohali",
    "chandigarh",
    "navi mumbai",

    # States/Regions (occasionally used)
    "karnataka",
    "maharashtra",
    "telangana",
    "tamil nadu",
    "kerala",
    "gujarat",
    "uttar pradesh",

    # Common abbreviations
    "blr",
    "hyd",
    "delhi ncr",
    "ncr",
]