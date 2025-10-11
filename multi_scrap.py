# multi_scrap.py
import os
from dotenv import load_dotenv
from scrapers.google_search_scraper import GoogleSearchScraper
from scrapers.search_scraper import SearchScraper  # Bing HTML
from scrapers.duckduckgo_scraper import DuckDuckGoScraper
from scrapers.jeune_afrique_scraper import JeuneAfriqueMultiCountryScraper
from core.storage import save_data
import sqlite3
from datetime import datetime

load_dotenv()

# ----- CONFIG -----
DATE_RANGE = os.getenv("DEFAULT_DATE_RANGE", "w1")
COUNTRIES = os.getenv("COUNTRIES").split(",")
MAX_PAGES = 2
PAGES_JA = 2
CACHE_DB = "cache.db"

# ----- CACHE UTILITIES -----
def init_cache():
    conn = sqlite3.connect(CACHE_DB)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cache (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT NOT NULL,
        query TEXT,
        url TEXT UNIQUE,
        title TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def save_to_cache(source, query, results):
    conn = sqlite3.connect(CACHE_DB)
    cursor = conn.cursor()
    for item in results:
        url = item.get("url") or item.get("link")
        title = item.get("title") or "No title"
        if not url:
            continue  # ignore si pas d'URL
        try:
            cursor.execute("""
                INSERT INTO cache (source, query, url, title) VALUES (?, ?, ?, ?)
            """, (source, query, url, title))
        except sqlite3.IntegrityError:
            continue  # URL déjà présente
    conn.commit()
    conn.close()


def load_from_cache(query, source=None):
    conn = sqlite3.connect(CACHE_DB)
    cursor = conn.cursor()
    if source:
        cursor.execute("SELECT title, url FROM cache WHERE query=? AND source=?", (query, source))
    else:
        cursor.execute("SELECT title, url FROM cache WHERE query=?", (query,))
    rows = cursor.fetchall()
    conn.close()
    return [{"title": r[0], "url": r[1]} for r in rows]

# ----- INIT -----
init_cache()

# ----- SCRAPING -----
for country in COUNTRIES:
    query = f"{country.strip()} économie"
    merged_results = []
    seen_urls = set()
    stats = {}

    # -------- GOOGLE API --------
    cached_google = load_from_cache(query, "google")
    if cached_google:
        merged_results.extend(cached_google)
        stats["google"] = len(cached_google)
    else:
        google_scraper = GoogleSearchScraper(query=query, date_range=DATE_RANGE)
        google_data = google_scraper.run()
        for item in google_data[query]:
            url = item.get("link")
            if url not in seen_urls:
                merged_results.append(item)
                seen_urls.add(url)
        save_to_cache("google", query, google_data[query])
        stats["google"] = len(google_data[query])

    # -------- BING HTML --------
    cached_bing = load_from_cache(query, "bing")
    if cached_bing:
        merged_results.extend(cached_bing)
        stats["bing"] = len(cached_bing)
    else:
        bing_scraper = SearchScraper(query=query, engine="bing")
        bing_data = bing_scraper.run()
        for item in bing_data[query]:
            url = item.get("url") or item.get("link")
            if url not in seen_urls:
                merged_results.append(item)
                seen_urls.add(url)
        save_to_cache("bing", query, bing_data[query])
        stats["bing"] = len(bing_data[query])

    # -------- DUCKDUCKGO HTML via DDGS --------
    cached_ddg = load_from_cache(query, "duckduckgo")
    if cached_ddg:
        merged_results.extend(cached_ddg)
        stats["duckduckgo"] = len(cached_ddg)
    else:
        ddg_scraper = DuckDuckGoScraper(query=query, max_results=20)
        ddg_data = ddg_scraper.run()
        for item in ddg_data[query]:
            url = item.get("url")
            if url not in seen_urls:
                merged_results.append(item)
                seen_urls.add(url)
        save_to_cache("duckduckgo", query, ddg_data[query])
        stats["duckduckgo"] = len(ddg_data[query])

    # -------- JEUNEAFRIQUE MULTI-PAGES --------
    ja_slug = country.strip().replace(" ", "-")
    cached_ja = load_from_cache(query, "jeuneafrique")
    if cached_ja:
        merged_results.extend(cached_ja)
        stats["jeuneafrique"] = len(cached_ja)
    else:
        ja_scraper = JeuneAfriqueMultiCountryScraper(slugs=[ja_slug], pages=PAGES_JA)
        ja_data = ja_scraper.run()
        ja_articles = ja_data[ja_slug]
        for item in ja_articles:
            url = item.get("url")
            if url not in seen_urls:
                merged_results.append(item)
                seen_urls.add(url)
        save_to_cache("jeuneafrique", query, ja_articles)
        stats["jeuneafrique"] = len(ja_articles)

    # ----- SAVE + LOG -----
    save_data(f"prod_{country.strip().replace(' ', '_')}", {query: merged_results})
    print(f"{len(merged_results)} résultats fusionnés pour '{query}' | stats: {stats}")
