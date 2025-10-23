# core/config.py
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# -------------------------------
# 🌐 Paramètres HTTP globaux
# -------------------------------
HTTP_CONFIG: Dict[str, Any] = {
    "timeout": int(os.getenv("HTTP_TIMEOUT", 10)),  # secondes
    "max_retries": int(os.getenv("HTTP_MAX_RETRIES", 3)),
    "retry_pause_range": (float(os.getenv("HTTP_RETRY_MIN", 2.0)),
                          float(os.getenv("HTTP_RETRY_MAX", 5.0))),
    "headers": {
        "User-Agent": os.getenv(
            "USER_AGENT",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
        )
    },
    "anti_429_pause_range": (float(os.getenv("ANTI_429_MIN", 4.0)),
                             float(os.getenv("ANTI_429_MAX", 8.0))),
}

# -------------------------------
# 🗂 Cache
# -------------------------------
CACHE_CONFIG: Dict[str, Any] = {
    "filepath": os.getenv("CACHE_FILE", "cache.json"),
    "use_cache": os.getenv("USE_CACHE", "true").lower() == "true",
}

# -------------------------------
# 🧰 Scraper Runner
# -------------------------------
SCRAPER_RUNNER_CONFIG: Dict[str, Any] = {
    "max_workers": int(os.getenv("MAX_WORKERS", 4)),
}

# -------------------------------
# 🔧 Autres constantes projet
# -------------------------------
PROJECT_NAME = "web-sniffer"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
