import os
from dotenv import load_dotenv
from scrapers.google_search_scraper import GoogleSearchScraper
from core.storage import save_data

load_dotenv()

def run_google_scraper(query="Burkina Faso économie", date_range=None, save_func=save_data):
    scraper = GoogleSearchScraper(query=query, date_range=date_range)
    data = scraper.run(max_pages=1)
    save_func(f"google_{query.replace(' ', '_')}", data)
    return data

# ----- BLOCK MAIN -----
if __name__ == "__main__":
    query = "Burkina Faso économie"
    data = run_google_scraper(query=query)
    print(f"[OK] {len(data[query])} résultats trouvés pour '{query}'")
    for i, item in enumerate(data[query], 1):
        print(f"{i}. {item['title']} ({item['url']})\n   {item['snippet']}\n")
