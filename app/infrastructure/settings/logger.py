import logging
from datetime import datetime

from app.infrastructure.settings.config import LOGGING_LEVEL


def setup_logging() -> None:
    log_filename = datetime.now().strftime("app/logs/logs_%Y-%m-%d_%H.log")
    
    logging.basicConfig(
        level=LOGGING_LEVEL,
        format="%(levelname)s | %(asctime)s | %(filename)s | %(message)s",
        handlers=[
            logging.FileHandler(log_filename, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    logging.info('Logging is configured')
