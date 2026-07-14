import hashlib
import re
from html.parser import HTMLParser
import httpx
from job_radar.config import PAGES, BOT_TOKEN, CHAT_ID
from job_radar.database import get_page_hash, save_page_hash
from job_radar.logger import logger

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.in_style_or_script = False

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.in_style_or_script = True

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.in_style_or_script = False

    def handle_data(self, data):
        if not self.in_style_or_script:
            self.text.append(data)

def extract_normalized_text(html: str) -> str:
    """Extract visible text from HTML and normalize whitespace."""
    parser = TextExtractor()
    parser.feed(html)
    text = " ".join(parser.text)
    return re.sub(r'\s+', ' ', text).strip()

def send_page_notification(name: str, url: str):
    """Send a Telegram notification that an opportunity page was updated."""
    if not BOT_TOKEN or not CHAT_ID:
        logger.warning("Telegram BOT_TOKEN or CHAT_ID is not configured. Skipping notification.")
        return
        
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    text = (
        f"🚨 <b>Opportunity Page Updated</b>\n\n"
        f"<b>Page:</b>\n{name}\n\n"
        f"<b>URL:</b>\n<a href='{url}'>{url}</a>\n\n"
        f"The page content has changed since the previous check."
    )
    
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    
    try:
        response = httpx.post(api_url, json=payload, timeout=10)
        response.raise_for_status()
        logger.info(f"Page notification sent for {name}")
    except Exception as e:
        logger.error(f"Failed to send page notification for {name}: {e}")

def check_pages():
    """Iterate through the configured pages and monitor them for text changes."""
    pages_checked = len(PAGES)
    pages_changed = 0
    notifications_sent = 0
    failures = 0
    
    for page in PAGES:
        name = page["name"]
        url = page["url"]
        
        try:
            logger.info(f"Checking page: {name}...")
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
            response = httpx.get(url, timeout=15, follow_redirects=True, headers=headers)
            response.raise_for_status()
            
            html = response.text
            text = extract_normalized_text(html)
            
            current_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
            previous_hash = get_page_hash(url)
            
            if previous_hash is None:
                # First run stores page hashes
                save_page_hash(url, current_hash)
                logger.info(f"First run for {name}: Stored initial hash.")
            elif current_hash != previous_hash:
                # Hash changed
                save_page_hash(url, current_hash)
                pages_changed += 1
                logger.info(f"Page content changed for {name}")
                send_page_notification(name, url)
                notifications_sent += 1
            else:
                logger.info(f"No changes for {name}")
                
        except Exception as e:
            logger.error(f"Failed to monitor page {name}: {e}")
            failures += 1

    summary = (
        f"\nPages Checked: {pages_checked}\n"
        f"Pages Changed: {pages_changed}\n"
        f"Notifications Sent: {notifications_sent}\n"
        f"Failures: {failures}\n"
    )
    logger.info(f"Page Monitor Summary:{summary}")
