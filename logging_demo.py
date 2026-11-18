
import logging
from logging_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

logger.debug("This is a debug message")
logger.info("Application started")
logger.warning("This is a warning")
logger.error("Something went wrong")
logger.critical("Critical error occurred")