import os
from dotenv import load_dotenv
from scrapers.google_search_scraper import GoogleSearchScraper
from scrapers.search_scraper import SearchScraper
from scrapers.jeune_afrique_scraper import JeuneAfriqueMultiCountryScraper
from core.storage import save_data
from core.logger import log_dev

load_dotenv()

DATE_RANGE = os.getenv("DEFAULT_DATE_RANGE", "w1")
COUNTRIES = os.getenv("COUNTRIES").split(",")
PAGES_JA = int(os.getenv("PAGES_JA", 2))
MOTORS = ["google", "bing", "duckduckgo", "jeuneafrique"]

if __name__ == "__main__":
    for country in COUNTRIES:
        query = f"{country.strip()} économie"
        print(f"\n--- {country.upper()} ---")

        merged_results = {}
        merged_results[query] = []
        seen_urls = set()
        stats = {}

        # 1️⃣ Google API
        google_scraper = GoogleSearchScraper(query=query, date_range=DATE_RANGE)
        google_data = google_scraper.run()
        for item in google_data[query]:
            url = item.get("link")
            if url not in seen_urls:
                merged_results[query].append(item)
                seen_urls.add(url)
        stats["google"] = len(google_data[query])

        # 2️⃣ Bing HTML
        bing_scraper = SearchScraper(query=query, engine="bing")
        bing_data = bing_scraper.run()
        for item in bing_data[query]:
            url = item.get("url") or item.get("link")
            if url not in seen_urls:
                merged_results[query].append(item)
                seen_urls.add(url)
        stats["bing"] = len(bing_data[query])

        # 3️⃣ DuckDuckGo HTML
        ddg_scraper = SearchScraper(query=query, engine="duckduckgo")
        ddg_data = ddg_scraper.run()
        for item in ddg_data[query]:
            url = item.get("url") or item.get("link")
            if url not in seen_urls:
                merged_results[query].append(item)
                seen_urls.add(url)
        stats["duckduckgo"] = len(ddg_data[query])

        # 4️⃣ JeuneAfrique multi-pages
        ja_scraper = JeuneAfriqueMultiCountryScraper(slugs=[country.strip().replace(" ", "-")], pages=PAGES_JA)
        ja_data = ja_scraper.run()
        ja_articles = ja_data[country.strip().replace(" ", "-")]
        for item in ja_articles:
            url = item.get("url")
            if url not in seen_urls:
                merged_results[query].append(item)
                seen_urls.add(url)
        stats["jeuneafrique"] = len(ja_articles)

        # Sauvegarde JSON
        save_data(f"prod_{country.strip().replace(' ', '_')}", merged_results)

        # Journal DEV automatique
        log_dev(f"{country.strip()} | {query} | fusionné {len(merged_results[query])} | stats: {stats}")

        print(f"{len(merged_results[query])} résultats fusionnés pour '{query}'")
