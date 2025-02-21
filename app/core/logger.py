import logging
from datetime import datetime


def setup_logging() -> None:
    log_filename = datetime.now().strftime("app/logs/logs_%Y-%m-%d_%H.%M.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | %(asctime)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    logging.info('Logging is configured')