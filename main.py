import os

from dotenv import load_dotenv

from core.storage import save_data
from scrapers.google_search_scraper import GoogleSearchScraper

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
CX = os.getenv("GOOGLE_CX_ID")
DATE_RANGE = os.getenv("DEFAULT_DATE_RANGE", "w1")
COUNTRIES = os.getenv("COUNTRIES", "burkina faso").split(",")


if __name__ == "__main__":
    for country in COUNTRIES:
        query = f"{country.strip()} économie"
        scraper = GoogleSearchScraper(query=query, date_range=DATE_RANGE)
        data = scraper.run()
        save_data(f"google_{country.strip().replace(' ', '_')}", data)
        print(f"{len(data[query])} résultats trouvés pour '{query}' sur Google.")
