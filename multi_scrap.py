# multi_scrap.py
import os
import threading
import time
from queue import Queue
from datetime import datetime
from dotenv import load_dotenv
import sqlite3

from scrapers.google_search_scraper import GoogleSearchScraper
from scrapers.search_scraper import SearchScraper
from scrapers.duckduckgo_scraper import DuckDuckGoScraper
from scrapers.jeune_afrique_scraper import JeuneAfriqueMultiCountryScraper
from core.cache import Cache
from core.utils import setup_logger

load_dotenv()

# ----- CONFIG -----
DATE_RANGE = os.getenv("DEFAULT_DATE_RANGE", "w1")
COUNTRIES = [c.strip() for c in os.getenv("COUNTRIES").split(",")]
MAX_PAGES = 2
PAGES_JA = 2
CACHE_DB = "cache.db"
RESULTS_DB = "results.db"
CACHE_TTL = 24 * 3600  # 24h
JA_REQUEST_INTERVAL = 2

# ----- INIT -----
logger = setup_logger()
cache = Cache(db_path=CACHE_DB, ttl_seconds=CACHE_TTL)

# ----- SQLite results DB -----
def init_results_db():
    conn = sqlite3.connect(RESULTS_DB)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        country TEXT,
        query TEXT,
        source TEXT,
        title TEXT,
        url TEXT UNIQUE,
        snippet TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def save_result(country, query, source, results):
    conn = sqlite3.connect(RESULTS_DB)
    cursor = conn.cursor()
    for item in results:
        try:
            cursor.execute("""
                INSERT INTO results (country, query, source, title, url, snippet)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (country, query, source, item["title"], item["url"], item.get("snippet", "")))
        except sqlite3.IntegrityError:
            continue  # URL déjà présente
    conn.commit()
    conn.close()

init_results_db()

# ----- WORKER FUNCTION -----
def scrape_country(country, output_queue):
    query = f"{country} securité"
    merged_results = []
    seen_urls = set()
    stats_per_source = {}

    scrapers = [
        ("google", GoogleSearchScraper, {"query": query, "date_range": DATE_RANGE}),
        ("bing", SearchScraper, {"query": query, "engine": "bing"}),
        ("duckduckgo", DuckDuckGoScraper, {"query": query, "max_results": 20}),
        ("jeuneafrique", JeuneAfriqueMultiCountryScraper, {"slugs": [country.replace(" ", "-")], "pages": PAGES_JA}),
    ]

    for source, scraper_class, kwargs in scrapers:
        try:
            cached = cache.load(query, source)
            if cached:
                merged_results.extend(cached)
                stats_per_source[source] = {"count": len(cached), "status": "SKIPPED"}
            else:
                if source == "google":
                    scraper = GoogleSearchScraper(**kwargs)
                    data = scraper.run(max_pages=MAX_PAGES)
                    items = data.get(query, [])
                elif source == "duckduckgo":
                    scraper = DuckDuckGoScraper(**kwargs)
                    data = scraper.run()
                    items = data.get(query, [])
                elif source == "jeuneafrique":
                    scraper = JeuneAfriqueMultiCountryScraper(**kwargs)
                    data = {}
                    slug = kwargs["slugs"][0]
                    for page in range(1, PAGES_JA + 1):
                        page_data = scraper.fetch(slug, page)
                        parsed = scraper.parse(page_data)
                        if slug not in data:
                            data[slug] = []
                        data[slug].extend(parsed)
                        time.sleep(JA_REQUEST_INTERVAL)  # intervalle anti-429
                    items = data.get(slug, [])
                else:
                    scraper = scraper_class(**kwargs)
                    data = scraper.run(max_pages=MAX_PAGES)
                    items = data.get(query, [])

                results = []
                for item in items:
                    url = item.get("url") or item.get("link")
                    title = item.get("title")
                    snippet = item.get("snippet", "")
                    if url and url not in seen_urls:
                        results.append({"title": title, "url": url, "snippet": snippet})
                        seen_urls.add(url)

                merged_results.extend(results)
                cache.save(query, source, results)
                save_result(country, query, source, results)
                stats_per_source[source] = {"count": len(results), "status": "OK"}

        except Exception as e:
            logger.error(f"{scraper_class.__name__} | {query} | ERROR | {e}")
            stats_per_source[source] = {"count": 0, "status": "ERROR"}

    output_queue.put((country, query, merged_results, stats_per_source))

# ----- THREADING -----
output_queue = Queue()
threads = []

for country in COUNTRIES:
    t = threading.Thread(target=scrape_country, args=(country, output_queue))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

# ----- LOG RESULTS -----
while not output_queue.empty():
    country, query, merged_results, stats = output_queue.get()
    logger.info(f"{country} | {query} | fusionné {len(merged_results)} | stats: {stats}")
