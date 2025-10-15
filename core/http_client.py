import logging
import requests
from typing import Optional
from core.config import HTTP_CONFIG

logger = logging.getLogger("http_client")

def fetch(
    url: str,
    timeout: Optional[float] = None,
    headers: Optional[dict] = None
) -> str:
    """
    Effectue une requête GET HTTP simple avec gestion du timeout et headers.
    Utilise les paramètres globaux de core/config.py si timeout ou headers non fournis.
    """
    timeout = timeout or HTTP_CONFIG["timeout"]
    headers = headers or HTTP_CONFIG["headers"]

    try:
        response = requests.get(url, timeout=timeout, headers=headers)
        response.raise_for_status()
        logger.info(f"[OK] {url}")
        return response.text
    except requests.RequestException as e:
        logger.error(f"[FAIL] {url} | {e}")
        raise
