import os
from typing import Any, Dict, List

from dotenv import load_dotenv

from core.http_client import fetch

load_dotenv()

class GoogleSearchScraper:
    def __init__(self, query: str, date_range: str = None):
        self.query: str = query
        self.api_key: str = os.getenv("GOOGLE_API_KEY", "")
        self.cx_id: str = os.getenv("GOOGLE_CX_ID", "")
        self.date_range: str = date_range or os.getenv("DEFAULT_DATE_RANGE", "w1")

    def fetch_page(self, start: int = 1) -> Any:
        url: str = "https://www.googleapis.com/customsearch/v1"
        params: Dict[str, str] = {
            "q": self.query,
            "cx": self.cx_id,
            "key": self.api_key,
            "dateRestrict": self.date_range,
            "start": str(start)
        }
        return fetch(url, params=params)

    def run(self, max_pages: int = 1) -> Dict[str, List[Dict[str, Any]]]:
        all_results: List[Dict[str, Any]] = []
        for page in range(max_pages):
            start = page * 10 + 1
            resp = self.fetch_page(start=start)
            try:
                data: Dict[str, Any] = resp.json()  # si fetch retourne requests.Response
            except Exception:
                import json
                data = json.loads(resp)  # fallback si string brut
            for item in data.get("items", []):
                all_results.append({
                    "title": item.get("title"),
                    "url": item.get("link"),
                    "snippet": item.get("snippet", "")
                })
        return {self.query: all_results}
