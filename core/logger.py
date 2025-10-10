
import os
from datetime import datetime

LOG_FILE = os.path.join("docs", "JOURNAL_DEV.md")  # ou un autre chemin

def log_dev(message: str):
    """
    Ajoute une entrée dans le journal DEV avec timestamp.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"- [{timestamp}] {message}\n")
