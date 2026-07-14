import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

# Ensure logs directory exists at project root
LOGS_DIR = Path(__file__).parent.parent.parent / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

def setup_logger():
    logger = logging.getLogger("job_radar")
    
    if logger.hasHandlers():
        return logger
        
    logger.setLevel(logging.INFO)
    
    # Daily log file (rotates at midnight)
    log_file = LOGS_DIR / "job_radar.log"
    file_handler = TimedRotatingFileHandler(
        log_file,
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8"
    )
    
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - [%(filename)s] - %(message)s"
    )
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()
