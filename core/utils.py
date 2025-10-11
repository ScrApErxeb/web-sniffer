# core/utils.py
import logging
from urllib.parse import urlparse, urlunparse

def setup_logger(name="web-sniffer"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s | %(message)s")
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger

def stats(results):
    """Retourne des stats simples sur les résultats"""
    return {
        "total": len(results),
        "titles": [r["title"] for r in results[:5]],  # 5 premiers titres
    }
# core/utils.py



def normalize_url(url: str) -> str:
    """
    Normalise une URL pour éviter les doublons :
    - Supprime les fragments (#)
    - Convertit le scheme et le netloc en minuscules
    - Supprime les paramètres inutiles
    """
    parsed = urlparse(url)
    cleaned = parsed._replace(fragment="")
    return urlunparse(cleaned).lower()
