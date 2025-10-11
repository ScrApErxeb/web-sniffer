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
                "snippet": item.get("snippet", "")  # ajout du snippet
            })
        return results


    def run(self, max_pages: int = 1):
        """
        Pagination Google API : récupère max_pages * 10 résultats
        """
        all_results = []
        for page in range(max_pages):
            start = page * 10 + 1  # Google API start index
            results = self.fetch(start=start)
            if not results:
                break
            all_results.extend(results)
        return {self.query: all_results}
