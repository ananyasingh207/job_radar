# Job Radar 📡

A modular job aggregation, filtering, and notification system designed to monitor top job boards, careers pages, and repositories, filtering specifically for tech roles in India and delivering instant updates via Telegram.

---

## 🚀 Features

- **Multi-Source Crawling:**
  - **Greenhouse:** Custom parser for Greenhouse job boards (e.g., PhonePe, Groww, Stripe, OpenAI).
  - **Workday:** Automated parsing of Workday career sites (e.g., Flipkart, JPMorgan Chase, Walmart).
  - **GitHub Repositories:** Pulls from curated listings like SimplifyJobs and SpeedyApply.
  - **Direct APIs:** Built-in integrations for Amazon (including the WoW program) and Microsoft.
  - **Page Monitor:** Detects page updates on static URLs (e.g., Apple Students, Microsoft Explore).
- **Smart Filtering:**
  - Standardizes location matching (focusing on major Indian tech hubs & remote India).
  - Matches roles using target keywords (e.g., SDE, Internship, Entry Level) while excluding irrelevant departments (e.g., marketing, sales, HR).
- **Deduplication:** Uses SQLite to store hashed job details and prevent duplicate notifications.
- **Telegram Notifications:** Instant, nicely-formatted job alert cards sent directly to your configured Telegram channel/chat.

---

## 🛠️ Tech Stack & Requirements

- **Python 3.11+**
- **HTTP client:** `httpx`
- **Environment config:** `python-dotenv`
- **Database:** SQLite (built-in)

---

## ⚙️ Setup & Installation

### 1. Clone & Navigate
```bash
git clone <repository-url>
cd "Job Radar"
```

### 2. Environment Configuration
Create a `.env` file in the root directory and populate it with your configuration keys:

```env
GITHUB_API=https://api.github.com
GITHUB_TOKEN=your_github_token
BOT_TOKEN=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id
```

### 3. Install Dependencies
Create a virtual environment and install the required modules:

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux

# Install requirements
pip install -r requirements.txt

# Or install editable package
pip install -e .
```

---

## 🏃 Running the Application

To start the Job Radar daemon:

```bash
# If installed in editable mode or running from the root with python path configured
python -m job_radar.main
```

The daemon runs continuously, checking all configured sources, saving target jobs, sending notifications, and sleeping for 5 minutes between cycles.

---

## 📁 Project Structure

```
Job Radar/
├── data/                  # SQLite DB storage (created automatically)
├── logs/                  # System log files
├── src/
│   └── job_radar/        # Core source code
│       ├── main.py        # Application daemon entrypoint
│       ├── config.py      # Company sources, keyword lists, and filters
│       ├── database.py    # SQLite integration & job deduplication
│       ├── notifier.py    # Telegram messenger integration
│       └── ...            # Dedicated parsers for Amazon, Workday, etc.
├── pyproject.toml         # Package configuration
└── requirements.txt       # Dependency definitions
```
