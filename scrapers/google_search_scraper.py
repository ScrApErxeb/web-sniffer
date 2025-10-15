from core.http_client import fetch
from core.parser import parse_google_results
import os
from dotenv import load_dotenv

load_dotenv()

class GoogleSearchScraper:
    def __init__(self, query: str, date_range: str = None):
        self.query = query
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.cx_id = os.getenv("GOOGLE_CX_ID")
        self.date_range = date_range or os.getenv("DEFAULT_DATE_RANGE", "w1")

    def fetch_page(self, start: int = 1):
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": self.query,
            "cx": self.cx_id,
            "key": self.api_key,
            "dateRestrict": self.date_range,
            "start": start
        }
        return fetch(url, params=params)

    def run(self, max_pages: int = 1):
        all_results = []
        for page in range(max_pages):
            start = page * 10 + 1
            resp = self.fetch_page(start=start)
            try:
                data = resp.json()
            except Exception:
                import json
                data = json.loads(resp)
            all_results.extend(parse_google_results(data))
        return {self.query: all_results}
