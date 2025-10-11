from .base_scraper import BaseScraper
from ddgs import DDGS

class DuckDuckGoScraper(BaseScraper):
    def __init__(self, query: str, max_results: int = 10):
        super().__init__(name="DuckDuckGoScraper")
        self.query = query
        self.max_results = max_results

    def run(self):
        with DDGS() as ddg:
            # ATTENTION : la méthode text() prend `query` comme argument positionnel
            results_raw = ddg.text(self.query, max_results=self.max_results)
        results = []
        for item in results_raw:
            title = item.get("title")
            url = item.get("href") or item.get("link")
            if title and url:
                results.append({"title": title, "url": url})
        return {self.query: results}

    def parse(self, html=None):
        return []
