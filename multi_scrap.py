# multi_scrap.py
import os
from dotenv import load_dotenv
from scrapers.google_search_scraper import GoogleSearchScraper
from scrapers.search_scraper import SearchScraper  # Bing HTML
from scrapers.duckduckgo_scraper import DuckDuckGoScraper
from scrapers.jeune_afrique_scraper import JeuneAfriqueMultiCountryScraper
from core.storage import save_data
from core.cache import Cache

load_dotenv()

# ----- CONFIG -----
DATE_RANGE = os.getenv("DEFAULT_DATE_RANGE", "w1")
COUNTRIES = os.getenv("COUNTRIES").split(",")
MAX_PAGES = 2
PAGES_JA = 2
CACHE_DB = "cache.db"
CACHE_TTL_HOURS = 24

# ----- INIT CACHE -----
cache = Cache(db_path=CACHE_DB, ttl_hours=CACHE_TTL_HOURS)

# ----- SCRAPING -----
for country in COUNTRIES:
    query = f"{country.strip()} économie"
    merged_results = []
    seen_urls = set()
    stats = {}

    # -------- GOOGLE API --------
    cached_google = cache.load(query, "google")
    if cached_google:
        merged_results.extend(cached_google)
        stats["google"] = len(cached_google)
    else:
        google_scraper = GoogleSearchScraper(query=query, date_range=DATE_RANGE)
        google_data = google_scraper.run(max_pages=MAX_PAGES)
        for item in google_data[query]:
            url = item.get("link")
            snippet = item.get("snippet", "")
            if url and url not in seen_urls:
                merged_results.append({"title": item["title"], "url": url, "snippet": snippet})
                seen_urls.add(url)
        cache.save("google", query, merged_results)
        stats["google"] = len(google_data[query])

    # -------- BING HTML --------
    cached_bing = cache.load(query, "bing")
    if cached_bing:
        merged_results.extend(cached_bing)
        stats["bing"] = len(cached_bing)
    else:
        bing_scraper = SearchScraper(query=query, engine="bing")
        bing_data = bing_scraper.run(max_pages=MAX_PAGES)
        for item in bing_data[query]:
            url = item.get("url")
            snippet = item.get("snippet", "")
            if url and url not in seen_urls:
                merged_results.append({"title": item["title"], "url": url, "snippet": snippet})
                seen_urls.add(url)
        cache.save("bing", query, bing_data[query])
        stats["bing"] = len(bing_data[query])

    # -------- DUCKDUCKGO HTML via DDGS --------
    cached_ddg = cache.load(query, "duckduckgo")
    if cached_ddg:
        merged_results.extend(cached_ddg)
        stats["duckduckgo"] = len(cached_ddg)
    else:
        ddg_scraper = DuckDuckGoScraper(query=query, max_results=20)
        ddg_data = ddg_scraper.run()
        for item in ddg_data[query]:
            url = item.get("url")
            snippet = item.get("snippet", "")
            if url and url not in seen_urls:
                merged_results.append({"title": item["title"], "url": url, "snippet": snippet})
                seen_urls.add(url)
        cache.save("duckduckgo", query, ddg_data[query])
        stats["duckduckgo"] = len(ddg_data[query])

    # -------- JEUNEAFRIQUE MULTI-PAGES --------
    ja_slug = country.strip().replace(" ", "-")
    cached_ja = cache.load(query, "jeuneafrique")
    if cached_ja:
        merged_results.extend(cached_ja)
        stats["jeuneafrique"] = len(cached_ja)
    else:
        ja_scraper = JeuneAfriqueMultiCountryScraper(slugs=[ja_slug], pages=PAGES_JA)
        ja_data = ja_scraper.run()
        ja_articles = ja_data[ja_slug]
        for item in ja_articles:
            url = item.get("url")
            snippet = item.get("snippet", "")
            if url and url not in seen_urls:
                merged_results.append({"title": item["title"], "url": url, "snippet": snippet})
                seen_urls.add(url)
        cache.save("jeuneafrique", query, ja_articles)
        stats["jeuneafrique"] = len(ja_articles)

    # ----- SAVE + LOG -----
    save_data(f"prod_{country.strip().replace(' ', '_')}", {query: merged_results})
    print(f"{len(merged_results)} résultats fusionnés pour '{query}' | stats: {stats}")
