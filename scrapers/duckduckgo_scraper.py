from .base_scraper import BaseScraper
from ddgs import DDGS

class DuckDuckGoScraper(BaseScraper):
    def __init__(self, query: str, max_results: int = 10):
        super().__init__(name="DuckDuckGoScraper")
        self.query = query
        self.max_results = max_results

    def run(self, max_pages: int = 1):
        max_results = max_pages * 10
        results = []
        with DDGS() as ddg:
            # text() prend query comme argument positionnel
            results_raw = ddg.text(self.query, max_results=max_results)

        seen_urls = set()
        for item in results_raw:
            title = item.get("title")
            url = item.get("href") or item.get("link")
            snippet = item.get("body") or ""  # ajout du snippet
            if title and url and url not in seen_urls:
                results.append({"title": title, "url": url, "snippet": snippet})
                seen_urls.add(url)

        return {self.query: results}

    def parse(self, html=None):
        # Placeholder pour compatibilité avec BaseScraper
        return []
