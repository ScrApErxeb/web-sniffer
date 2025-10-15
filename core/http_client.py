# core/http_client.py
import requests
from loguru import logger
from config import HEADERS

def fetch(url: str, timeout: int = 10, params: dict = None) -> str | None:
    """
    Requête HTTP GET avec headers par défaut, paramètres optionnels et logging.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout, params=params)
        response.raise_for_status()
        logger.info(f"[OK] {url}")
        return response.text
    except Exception as e:
        logger.error(f"[ERROR] {url} → {e}")
        return None
