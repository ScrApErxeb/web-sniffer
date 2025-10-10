import requests
import os
from dotenv import load_dotenv

load_dotenv()

class GoogleSearchScraper:
    def __init__(self, query="Burkina Faso économie", date_range=None):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.cx_id = os.getenv("GOOGLE_CX_ID")
        self.query = query
        self.date_range = date_range or os.getenv("DEFAULT_DATE_RANGE", "w1")

    def fetch(self):
        params = {
            "q": self.query,
            "cx": self.cx_id,
            "key": self.api_key,
            "dateRestrict": self.date_range
        }
        resp = requests.get("https://www.googleapis.com/customsearch/v1", params=params)
        resp.raise_for_status()
        data = resp.json()
        results = []
        for item in data.get("items", []):
            results.append({"title": item["title"], "link": item["link"]})
        return results

    def run(self):
        results = self.fetch()
        return {self.query: results}  # maintenant data[query] fonctionne

