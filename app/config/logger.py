# src/utils/logger.py
import logging
import os

# Create logs directory if not exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger with both console and file handlers.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        # Set logging level and format
        logger.setLevel(logging.DEBUG)

        # Formatter for logs
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(log_format)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

        # File Handler
        file_handler = logging.FileHandler(os.path.join(LOG_DIR, "app.log"))
        file_handler.setLevel(logging.DEBUG)  # Capture detailed logs in file
        file_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        # Avoid duplicated logs
        logger.propagate = False

    return logger
