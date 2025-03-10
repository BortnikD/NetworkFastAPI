import logging
from datetime import datetime


def setup_logging(level: logging) -> None:
    log_filename = datetime.now().strftime("app/logs/logs_%Y-%m-%d_%H.log")
    
    logging.basicConfig(
        level=level,
        format="%(levelname)s | %(asctime)s | %(filename)s | %(message)s",
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    logging.info('Logging is configured')
