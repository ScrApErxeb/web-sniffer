# run_google_scraper.py
import os
from dotenv import load_dotenv
import requests

load_dotenv()

class GoogleSearchScraper:
    def __init__(self, query="Burkina Faso économie", date_range=None):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.cx_id = os.getenv("GOOGLE_CX_ID")
        self.query = query
        self.date_range = date_range or None  # facultatif

    def fetch(self, start: int = 1):
        params = {
            "q": self.query,
            "cx": self.cx_id,
            "key": self.api_key,
            "dateRestrict": self.date_range,
            "start": start
        }
        resp = requests.get("https://www.googleapis.com/customsearch/v1", params=params)
        resp.raise_for_status()
        data = resp.json()
        results = []
        for item in data.get("items", []):
            results.append({
                "title": item.get("title"),
                "url": item.get("link"),
                "snippet": item.get("snippet", "")
            })
        return results

    def run(self, max_pages: int = 1):
        all_results = []
        for page in range(max_pages):
            start = page * 10 + 1
            results = self.fetch(start=start)
            if not results:
                break
            all_results.extend(results)
        return {self.query: all_results}


if __name__ == "__main__":
    query = "Burkina Faso économie"
    scraper = GoogleSearchScraper(query=query, date_range=None)
    data = scraper.run(max_pages=1)
    print(f"{len(data[query])} résultats pour '{query}':")
    for i, item in enumerate(data[query], 1):
        print(f"{i}. {item['title']} ({item['url']})\n   {item['snippet']}\n")
