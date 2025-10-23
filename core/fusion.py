# core/fusion.py
from urllib.parse import urlparse


def normalize_url(url):
    """Supprime les paramètres et normalise l'URL pour éviter les doublons"""
    try:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    except Exception:
        return url

def merge_results(list_of_results):
    """Fusionne plusieurs listes de résultats et supprime les doublons"""
    seen_urls = set()
    merged = []
    for results in list_of_results:
        for item in results:
            url = normalize_url(item.get("url"))
            if url and url not in seen_urls:
                seen_urls.add(url)
                merged.append({
                    "title": item.get("title"),
                    "url": url,
                    "snippet": item.get("snippet", "")
                })
    return merged
