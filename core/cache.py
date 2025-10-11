# core/cache.py
import time
from typing import Any

class CacheEntry:
    def __init__(self, value: Any, ttl: int):
        self.value = value
        self.expiry = time.time() + ttl

    def is_valid(self):
        return time.time() < self.expiry

class Cache:
    _store = {}

    @classmethod
    def get(cls, key: str):
        entry = cls._store.get(key)
        if entry and entry.is_valid():
            return entry.value
        elif entry:
            del cls._store[key]  # TTL expiré
        return None

    @classmethod
    def set(cls, key: str, value: Any, ttl: int = 3600):
        cls._store[key] = CacheEntry(value, ttl)

    @classmethod
    def clear(cls):
        cls._store = {}
