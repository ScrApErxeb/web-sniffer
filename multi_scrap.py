# multi_scrap.py
import os
from dotenv import load_dotenv
from scrapers.google_search_scraper import GoogleSearchScraper
from scrapers.search_scraper import SearchScraper  # Bing HTML
from scrapers.duckduckgo_scraper import DuckDuckGoScraper
from scrapers.jeune_afrique_scraper import JeuneAfriqueMultiCountryScraper
from core.cache import Cache
from core.fusion import merge_results
from core.utils import setup_logger, normalize_url
from datetime import datetime

# ----- LOAD ENV -----
load_dotenv()
DATE_RANGE = os.getenv("DEFAULT_DATE_RANGE", "w1")
COUNTRIES = [c.strip() for c in os.getenv("COUNTRIES").split(",")]
MAX_PAGES = 2
PAGES_JA = 2
CACHE_TTL = int(os.getenv("CACHE_TTL_SECONDS", 3600))

# ----- LOGGER -----
logger = setup_logger("multi_scrap")

# ----- CACHE -----
cache = Cache(ttl_seconds=CACHE_TTL)

# ----- SCRAPING -----
for country in COUNTRIES:
    query = f"{country} économie"
    merged_results = []
    seen_urls = set()
    stats = {}

    # --- GOOGLE API ---
    cached_google = cache.load(query, "google")
    if cached_google:
        merged_results.extend(cached_google)
        stats["google"] = len(cached_google)
    else:
        scraper = GoogleSearchScraper(query=query, date_range=DATE_RANGE)
        data = scraper.run(max_pages=MAX_PAGES)[query]
        normalized = []
        for item in data:
            url = item.get("link")
            if url and url not in seen_urls:
                normalized.append({
                    "title": item.get("title", "No title"),
                    "url": normalize_url(url),
                    "snippet": item.get("snippet", "")
                })
                seen_urls.add(url)
        merged_results.extend(normalized)
        stats["google"] = len(normalized)
        cache.save(query, "google", normalized)

    # --- BING ---
    cached_bing = cache.load(query, "bing")
    if cached_bing:
        merged_results.extend(cached_bing)
        stats["bing"] = len(cached_bing)
    else:
        scraper = SearchScraper(query=query, engine="bing")
        data = scraper.run(max_pages=MAX_PAGES)[query]
        normalized = []
        for item in data:
            url = item.get("url") or item.get("link")
            if url and url not in seen_urls:
                normalized.append({
                    "title": item.get("title", "No title"),
                    "url": normalize_url(url),
                    "snippet": item.get("snippet", "")
                })
                seen_urls.add(url)
        merged_results.extend(normalized)
        stats["bing"] = len(normalized)
        cache.save(query, "bing", normalized)

    # --- DUCKDUCKGO ---
    cached_ddg = cache.load(query, "duckduckgo")
    if cached_ddg:
        merged_results.extend(cached_ddg)
        stats["duckduckgo"] = len(cached_ddg)
    else:
        scraper = DuckDuckGoScraper(query=query, max_results=20)
        data = scraper.run()[query]
        normalized = []
        for item in data:
            url = item.get("url")
            if url and url not in seen_urls:
                normalized.append({
                    "title": item.get("title", "No title"),
                    "url": normalize_url(url),
                    "snippet": item.get("snippet", "")
                })
                seen_urls.add(url)
        merged_results.extend(normalized)
        stats["duckduckgo"] = len(normalized)
        cache.save(query, "duckduckgo", normalized)

    # --- JEUNEAFRIQUE MULTI-PAGES ---
    slug = country.replace(" ", "-")
    cached_ja = cache.load(query, "jeuneafrique")
    if cached_ja:
        merged_results.extend(cached_ja)
        stats["jeuneafrique"] = len(cached_ja)
    else:
        scraper = JeuneAfriqueMultiCountryScraper(slugs=[slug], pages=PAGES_JA)
        data = scraper.run()[slug]
        normalized = []
        for item in data:
            url = item.get("url")
            if url and url not in seen_urls:
                normalized.append({
                    "title": item.get("title", "No title"),
                    "url": normalize_url(url),
                    "snippet": item.get("snippet", "")
                })
                seen_urls.add(url)
        merged_results.extend(normalized)
        stats["jeuneafrique"] = len(normalized)
        cache.save(query, "jeuneafrique", normalized)

    # ----- LOG + SAVE -----
    logger.info(f"{country} | {query} | fusionné {len(merged_results)} | stats: {stats}")
    print(f"{len(merged_results)} résultats fusionnés pour '{query}' | stats: {stats}")
