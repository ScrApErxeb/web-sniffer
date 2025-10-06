from loguru import logger
from config import LOG_PATH

logger.add(LOG_PATH, rotation="1 MB", level="INFO", enqueue=True)
