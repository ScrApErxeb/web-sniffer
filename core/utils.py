# core/utils.py
from core.cache import Cache

def cached_run(scraper, ttl: int = 3600):
    """
    Exécute un scraper avec cache TTL.
    """
    key = f"{scraper.name}:{getattr(scraper, 'query', 'multi')}"
    cached = Cache.get(key)
    if cached:
        return cached
    data = scraper.run()
    Cache.set(key, data, ttl)
    return data
