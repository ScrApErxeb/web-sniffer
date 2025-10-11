import os
from dotenv import load_dotenv
from scrapers.google_search_scraper import GoogleSearchScraper
from scrapers.search_scraper import SearchScraper
from scrapers.duckduckgo_scraper import DuckDuckGoScraper
from scrapers.jeune_afrique_scraper import JeuneAfriqueMultiCountryScraper
from core.cache import Cache
from core.utils import setup_logger
from core.reporting import Reporter
from core.storage import save_data

load_dotenv()

# ----- CONFIG -----
DATE_RANGE = os.getenv("DEFAULT_DATE_RANGE", "w1")
COUNTRIES = [c.strip() for c in os.getenv("COUNTRIES").split(",")]
MAX_PAGES = 2
PAGES_JA = 2
CACHE_DB = "cache.db"
CACHE_TTL = 24 * 3600  # 24h

# ----- INIT -----
logger = setup_logger()
cache = Cache(db_path=CACHE_DB, ttl_seconds=CACHE_TTL)
reporter = Reporter(output_dir="reports")

SCRAPERS = [
    ("google", GoogleSearchScraper, {"date_range": DATE_RANGE}),
    ("bing", SearchScraper, {"engine": "bing"}),
    ("duckduckgo", DuckDuckGoScraper, {"max_results": 20}),
    ("jeuneafrique", JeuneAfriqueMultiCountryScraper, {"pages": PAGES_JA}),
]

# ----- SCRAPING -----
for country in COUNTRIES:
    query = f"{country} économie"
    merged_results = []
    seen_urls = set()
    stats_per_source = {}

    for source_name, ScraperClass, kwargs in SCRAPERS:
        try:
            cached = cache.load(query, source_name)
            if cached:
                merged_results.extend(cached)
                stats_per_source[source_name] = {"count": len(cached), "status": "SKIPPED"}
                continue

            # Instanciation du scraper
            if source_name == "jeuneafrique":
                kwargs["slugs"] = [country.replace(" ", "-")]
            scraper = ScraperClass(query=query, **kwargs) if source_name != "jeuneafrique" else ScraperClass(**kwargs)
            data = scraper.run(max_pages=MAX_PAGES) if source_name != "jeuneafrique" else scraper.run()
            
            results = []
            items = data.get(query, data.get(country.replace(" ", "-"), []))
            for item in items:
                url = item.get("url") or item.get("link")
                title = item.get("title")
                snippet = item.get("snippet", "")
                if url and url not in seen_urls:
                    results.append({"title": title, "url": url, "snippet": snippet})
                    seen_urls.add(url)

            merged_results.extend(results)
            cache.save(query, source_name, results)
            stats_per_source[source_name] = {"count": len(results), "status": "OK"}
        except Exception as e:
            logger.error(f"{source_name.capitalize()}Scraper | {query} | ERROR | {e}")
            stats_per_source[source_name] = {"count": 0, "status": "ERROR"}

    # ----- SAVE + LOG + REPORT -----
    save_data(f"prod_{country.replace(' ', '_')}", {query: merged_results})
    logger.info(f"{country} | {query} | fusionné {len(merged_results)} | stats: {stats_per_source}")
    reporter.add_query_results(query, merged_results, stats_per_source)

# ----- GENERATE REPORT -----
json_file, html_file = reporter.save_all()
logger.info(f"Rapports générés: {json_file}, {html_file}")
