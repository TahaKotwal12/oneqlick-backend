# src/utils/logger.py
import logging
import os

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger with console handler and optional file handler.
    For serverless environments like Vercel, only console logging is used.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        # Set logging level and format
        logger.setLevel(logging.DEBUG)

        # Formatter for logs
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(log_format)

        # Console Handler (always available)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File Handler (only in non-serverless environments)
        # Check if we're in a serverless environment (Vercel, Lambda, etc.)
        is_serverless = (
            os.getenv("VERCEL") == "1" or 
            os.getenv("AWS_LAMBDA_FUNCTION_NAME") is not None or
            os.getenv("LAMBDA_RUNTIME_DIR") is not None
        )
        
        if not is_serverless:
            try:
                # Try to create logs directory for local development
                LOG_DIR = "logs"
                os.makedirs(LOG_DIR, exist_ok=True)
                
                file_handler = logging.FileHandler(os.path.join(LOG_DIR, "app.log"))
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            except (OSError, PermissionError):
                # If we can't write to file system, just use console logging
                pass

        # Avoid duplicated logs
        logger.propagate = False

    return logger
