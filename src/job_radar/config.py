from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_API = os.getenv("GITHUB_API")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

COMPANIES = [
    # GitHub
    {
        "name": "Simplify Summer 2026",
        "source": "github",
        "owner": "SimplifyJobs",
        "repo": "Summer2026-Internships",
        "branch": "dev",
        "path": ".github/scripts/listings.json",
        "priority": 1,
    },
    {
        "name": "Simplify New Grad",
        "source": "github",
        "owner": "SimplifyJobs",
        "repo": "New-Grad-Positions",
        "branch": "main",
        "path": ".github/scripts/listings.json",
        "priority": 1,
    },
    {
        "name": "SpeedyApply SWE Jobs",
        "source": "github",
        "owner": "speedyapply",
        "repo": "2026-SWE-College-Jobs",
        "branch": "main",
        "path": ".github/scripts/listings.json",
        "priority": 1,
    },

    # Greenhouse
    {"name": "PhonePe", "source": "greenhouse", "board": "phonepe", "priority": 1},
    {"name": "Groww", "source": "greenhouse", "board": "groww", "priority": 1},
    {"name": "Stripe", "source": "greenhouse", "board": "stripe", "priority": 1},
    {"name": "Cloudflare", "source": "greenhouse", "board": "cloudflare", "priority": 1},
    {"name": "MongoDB", "source": "greenhouse", "board": "mongodb", "priority": 1},
    {"name": "Datadog", "source": "greenhouse", "board": "datadog", "priority": 1},
    {"name": "Plaid", "source": "greenhouse", "board": "plaid", "priority": 1},
    {"name": "Brex", "source": "greenhouse", "board": "brex", "priority": 1},
    {"name": "Ramp", "source": "greenhouse", "board": "ramp", "priority": 1},
    {"name": "Grammarly", "source": "greenhouse", "board": "grammarly", "priority": 1},
    {"name": "Canva", "source": "greenhouse", "board": "canva", "priority": 1},
    {"name": "Dropbox", "source": "greenhouse", "board": "dropbox", "priority": 1},
    {"name": "Figma", "source": "greenhouse", "board": "figma", "priority": 1},
    {"name": "Airtable", "source": "greenhouse", "board": "airtable", "priority": 1},
    {"name": "Miro", "source": "greenhouse", "board": "miro", "priority": 1},
    {"name": "Notion", "source": "greenhouse", "board": "notion", "priority": 1},
    {"name": "Cockroach Labs", "source": "greenhouse", "board": "cockroachlabs", "priority": 1},
    {"name": "LaunchDarkly", "source": "greenhouse", "board": "launchdarkly", "priority": 1},
    {"name": "Redis", "source": "greenhouse", "board": "redis", "priority": 1},
    {"name": "GitLab", "source": "greenhouse", "board": "gitlab", "priority": 1},
    {"name": "HashiCorp", "source": "greenhouse", "board": "hashicorp", "priority": 1},
    {"name": "Elastic", "source": "greenhouse", "board": "elastic", "priority": 1},
    {"name": "Confluent", "source": "greenhouse", "board": "confluent", "priority": 1},
    {"name": "Snowflake", "source": "greenhouse", "board": "snowflake", "priority": 1},
    {"name": "Fivetran", "source": "greenhouse", "board": "fivetran", "priority": 1},
    {"name": "Cohere", "source": "greenhouse", "board": "cohere", "priority": 1},
    {"name": "Anthropic", "source": "greenhouse", "board": "anthropic", "priority": 1},
    {"name": "Hugging Face", "source": "greenhouse", "board": "huggingface", "priority": 1},
    {"name": "OpenAI", "source": "greenhouse", "board": "openai", "priority": 1},
    {"name": "Perplexity", "source": "greenhouse", "board": "perplexity", "priority": 1},

    # Workday Companies
    {"name": "Flipkart", "source": "workday", "careers_url": "https://flipkart.wd3.myworkdayjobs.com/Flipkart", "priority": 1},
    {"name": "Myntra", "source": "workday", "careers_url": "https://myntra.wd3.myworkdayjobs.com/Myntra", "priority": 1},
    {"name": "Morgan Stanley", "source": "workday", "careers_url": "https://ms.wd1.myworkdayjobs.com/MorganStanley", "priority": 1},
    {"name": "JPMorgan Chase", "source": "workday", "careers_url": "https://jpmc.wd1.myworkdayjobs.com/Careers", "priority": 1},
    {"name": "Adobe", "source": "workday", "careers_url": "https://adobe.wd5.myworkdayjobs.com/external_we", "priority": 1},
    {"name": "Walmart Global Tech", "source": "workday", "careers_url": "https://walmart.wd5.myworkdayjobs.com/WalmartExternal", "priority": 1},
    {"name": "Qualcomm", "source": "workday", "careers_url": "https://qualcomm.wd5.myworkdayjobs.com/External", "priority": 1},
    {"name": "Cisco", "source": "workday", "careers_url": "https://cisco.wd1.myworkdayjobs.com/GlobalCareers", "priority": 1},
    {"name": "Salesforce", "source": "workday", "careers_url": "https://salesforce.wd1.myworkdayjobs.com/External_Career_Site", "priority": 1},
    {"name": "Visa", "source": "workday", "careers_url": "https://visa.wd1.myworkdayjobs.com/visa", "priority": 1},

    # Future Custom Sources
    {"name": "Amazon", "source": "custom", "priority": 1},
    {"name": "Microsoft", "source": "custom", "priority": 1},
    {"name": "Google", "source": "custom", "priority": 1},
    {"name": "Razorpay", "source": "custom", "priority": 1},
    {"name": "CRED", "source": "custom", "priority": 1},
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



PAGES = [
    {
        "name": "Amazon WoW",
        "url": "https://amazon.jobs/content/en/career-programs/university/women-of-the-world",
    },
    {
        "name": "Amazon University Talent",
        "url": "https://www.amazon.jobs/content/en/career-programs/university?country[]=IN",
    },
    {
        "name": "Microsoft Explore",
        "url": "https://careers.microsoft.com/v2/global/en/exploremicrosoft",
    },
    {
        "name": "Apple Students",
        "url": "https://www.apple.com/careers/in/",
    }
]

AMAZON_CONFIG = {
    "enabled": True,
    "country": "India",
    "priority": 1,
}

MICROSOFT_CONFIG = {
    "enabled": True,
    "priority": 1,
    "country": "India",
}