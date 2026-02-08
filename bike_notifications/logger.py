import logging
from pathlib import Path
import sys
import asyncio

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = PROJECT_ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)

GENERAL_LOG = LOGS_DIR / "general.log"
ERROR_LOG = LOGS_DIR / "error.log"


def setup_logging():
    """Configure logging with separate handlers for general and error logs."""
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    general_handler = logging.FileHandler(GENERAL_LOG)
    general_handler.setLevel(logging.INFO)
    general_handler.setFormatter(formatter)

    error_handler = logging.FileHandler(ERROR_LOG)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    root_logger.addHandler(general_handler)
    root_logger.addHandler(error_handler)
    root_logger.addHandler(console_handler)
    
    return root_logger

def get_logger(name):
    """Get a named logger instance."""
    return logging.getLogger(name)

def add_exception_handler(logger: logging.Logger):
    """Add a handler for uncaught exceptions."""
    def handle_exception(exc_type, exc_value, exc_traceback):
        """Forward uncaught exceptions to the logger."""
        # Let Ctrl+C still behave normally
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logger.critical(
            "Uncaught exception",
            exc_info=(exc_type, exc_value, exc_traceback),
        )

    sys.excepthook = handle_exception


def add_async_exception_handler(logger: logging.Logger):
    """Add a handler for unhandled async exceptions."""
    def handle_async_exception(loop, context):
        """Forward unhandled async exceptions to the logger."""
        msg = context.get("exception", context["message"])
        logger.error("Unhandled async exception", exc_info=msg)

    asyncio.get_event_loop().set_exception_handler(handle_async_exception)
