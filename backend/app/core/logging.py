import sys
from loguru import logger

def setup_logging():
    # Remove default handler
    logger.remove()
    
    # Add structured logging to stdout
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
    )
    
    # Add file logging for errors with auto-directory creation
    import os
    os.makedirs("logs", exist_ok=True)
    logger.add(
        "logs/error.log",
        rotation="10 MB",
        retention="1 week",
        level="ERROR",
        compression="zip",
    )

setup_logging()
