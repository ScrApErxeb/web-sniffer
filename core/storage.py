import json
import os

from config import DATA_PATH


def save_data(source: str, data: dict) -> None:
    # Crée le dossier parent si nécessaire
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    try:
        with open(DATA_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps({source: data}, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"Erreur sauvegarde : {e}")
