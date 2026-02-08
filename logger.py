import logging
from pathlib import Path

LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

SUCCESS_LOG = LOGS_DIR / "success.log"
ERROR_LOG = LOGS_DIR / "error.log"


def setup_logging():
    """Configure logging with separate handlers for success and errors."""
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    success_handler = logging.FileHandler(SUCCESS_LOG)
    success_handler.setLevel(logging.DEBUG)
    success_handler.setFormatter(formatter)
    success_handler.addFilter(lambda record: record.levelno <= logging.INFO)
    
    error_handler = logging.FileHandler(ERROR_LOG)
    error_handler.setLevel(logging.WARNING)
    error_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    root_logger.addHandler(success_handler)
    root_logger.addHandler(error_handler)
    root_logger.addHandler(console_handler)
    
    return root_logger


def get_logger(name):
    """Get a named logger instance."""
    return logging.getLogger(name)