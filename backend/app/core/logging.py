# backend/app/core/logging.py

import logging

def setup_logging():
    """
    Set up logging for the application.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger("trading_logger")
    return logger
