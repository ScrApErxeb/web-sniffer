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

def merge_results(merged, new_results, seen_urls):
    for item in new_results:
        url = item.get("url") or item.get("link")
        if url and url not in seen_urls:
            merged.append(item)
            seen_urls.add(url)
    return merged
