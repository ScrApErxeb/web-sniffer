# core/cache.py
from typing import Any, Optional
import json
import os

class CacheInterface:
    def load(self, query: str, source: str) -> Optional[Any]:
        raise NotImplementedError

    def save(self, query: str, source: str, data: Any):
        raise NotImplementedError

# Exemple simple de cache en JSON
class JSONCache(CacheInterface):
    def __init__(self, filepath="cache.json"):
        self.filepath = filepath
        self._data = {}
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                self._data = json.load(f)

    def load(self, query: str, source: str):
        return self._data.get(query, {}).get(source)

    def save(self, query: str, source: str, data):
        if query not in self._data:
            self._data[query] = {}
        self._data[query][source] = data
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)
