# backend/app/utils/logger.py

import logging

def setup_logger(name: str, log_level: str = "INFO") -> logging.Logger:
    """
    Sets up a logger to log events to a file and console.
    """
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    file_handler = logging.FileHandler(f"logs/{name}.log")
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    logger.addHandler(file_handler)
    logger.setLevel(log_level)
    
    return logger
