import logging
import os

LOG_PATH = os.path.join("data", "logs", "web_sniffer.log")
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

logger = logging.getLogger("web_sniffer")
logger.setLevel(logging.INFO)

fh = logging.FileHandler(LOG_PATH, encoding="utf-8")
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

# Console
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
