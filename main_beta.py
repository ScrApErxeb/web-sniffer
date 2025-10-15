import os

from dotenv import load_dotenv

from core.storage import save_data
from scrapers.google_search_scraper import GoogleSearchScraper
from scrapers.jeune_afrique_scraper import JeuneAfriqueMultiCountryScraper
from scrapers.search_scraper import SearchScraper  # DuckDuckGo + Bing

load_dotenv()

DATE_RANGE = os.getenv("DEFAULT_DATE_RANGE", "w1")
COUNTRIES = os.getenv("COUNTRIES").split(",")

if __name__ == "__main__":
    for country in COUNTRIES:
        query = f"{country.strip()} économie"

        # Google officiel via API
        google_scraper = GoogleSearchScraper(query=query, date_range=DATE_RANGE)
        google_data = google_scraper.run()

        # Bing et DuckDuckGo via SearchScraper
        bing_scraper = SearchScraper(query=query, engine="bing")
        bing_data = bing_scraper.run()
        ddg_scraper = SearchScraper(query=query, engine="duckduckgo")
        ddg_data = ddg_scraper.run()

        # JeuneAfrique multi-pays
        ja_scraper = JeuneAfriqueMultiCountryScraper(slugs=[country.strip().replace(" ", "-")])
        ja_data = ja_scraper.run()
        ja_articles = ja_data[country.strip().replace(" ", "-")]

        # Fusionner et dédupliquer
        merged_results = {}
        merged_results[query] = []
        seen_urls = set()

        for source in [google_data[query], bing_data[query], ddg_data[query], ja_articles]:
            for item in source:
                url = item.get("link") or item.get("url")
                if url and url not in seen_urls:
                    merged_results[query].append(item)
                    seen_urls.add(url)

        save_data(f"beta_{country.strip().replace(' ', '_')}", merged_results)
        print(f"{len(merged_results[query])} résultats fusionnés pour '{query}'")
