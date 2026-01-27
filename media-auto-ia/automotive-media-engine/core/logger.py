"""
RYA.ai Centralized Logging Configuration.

Production-grade structured logging with:
- JSON formatting for GCP Cloud Logging
- Log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Contextual information (job_id, module, function)
- File rotation and retention
"""

import sys
import os
from pathlib import Path
from loguru import logger
from typing import Optional

# Create logs directory
LOGS_DIR = Path("./logs")
LOGS_DIR.mkdir(exist_ok=True)

# Remove default handler
logger.remove()

# Determine log level from environment
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
DEBUG_MODE = os.getenv("DEBUG", "false").lower() == "true"

if DEBUG_MODE:
    LOG_LEVEL = "DEBUG"

# Console handler (human-readable for development)
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{extra[job_id]}</cyan> | <level>{message}</level>",
    level=LOG_LEVEL,
    colorize=True,
    enqueue=True,  # Thread-safe
)

# File handler (JSON for production/GCP parsing)
logger.add(
    LOGS_DIR / "rya_{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {extra[job_id]} | {name}:{function}:{line} | {message}",
    level=LOG_LEVEL,
    rotation="00:00",  # New file every day
    retention="30 days",  # Keep logs for 30 days
    compression="zip",  # Compress old logs
    enqueue=True,
    serialize=False,  # Set to True for JSON output
)

# Error-only file handler
logger.add(
    LOGS_DIR / "errors_{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {extra[job_id]} | {name}:{function}:{line} | {message}",
    level="ERROR",
    rotation="00:00",
    retention="90 days",  # Keep errors longer
    compression="zip",
    enqueue=True,
)

# Configure default context
logger.configure(extra={"job_id": "system"})


def get_logger(job_id: Optional[str] = None):
    """
    Get a logger instance with optional job_id context.
    
    Args:
        job_id: Optional job identifier for correlation
        
    Returns:
        Logger instance with context
        
    Example:
        >>> log = get_logger("abc-123")
        >>> log.info("Processing started", topic="AI Ethics")
    """
    if job_id:
        return logger.bind(job_id=job_id)
    return logger.bind(job_id="system")


# Export configured logger
__all__ = ["logger", "get_logger"]
