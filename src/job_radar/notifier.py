import httpx
from job_radar.config import BOT_TOKEN, CHAT_ID
from job_radar.models import Job
from job_radar.logger import logger

def send_job(job: Job):
    """
    Send a nicely formatted job notification to Telegram.
    Continues running (fails gracefully) if Telegram request fails.
    """
    if not BOT_TOKEN or not CHAT_ID:
        logger.warning("Telegram BOT_TOKEN or CHAT_ID is not configured. Skipping notification.")
        return
        
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    text = (
        f"🌟 <b>New Job Alert</b>\n\n"
        f"<b>Company:</b> {job.company}\n"
        f"<b>Role:</b> {job.role}\n"
        f"<b>Location:</b> {job.location}\n"
        f"<b>Source:</b> {job.source}\n\n"
        f"<a href='{job.apply_url}'>Apply Here</a>"
    )
    
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    
    try:
        response = httpx.post(url, json=payload, timeout=10)
        response.raise_for_status()
        logger.info(f"Notification sent for {job.company} - {job.role}")
    except Exception as e:
        logger.error(f"Failed to send Telegram notification for {job.company}: {e}")
