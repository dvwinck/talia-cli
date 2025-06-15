"""Logging configuration for TaskListAI."""

import logging
import os
from pathlib import Path

# Create logs directory in user's home
LOGS_DIR = os.path.expanduser("~/.tasklistai/logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# Configure logging
def setup_logger():
    """Configure the logger for TaskListAI."""
    logger = logging.getLogger("tasklistai")
    logger.setLevel(logging.INFO)

    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(
        os.path.join(LOGS_DIR, "tasklistai.log"),
        encoding='utf-8'
    )

    # Create formatters and add it to handlers
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(log_format)
    file_handler.setFormatter(log_format)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# Create and configure logger
logger = setup_logger() 