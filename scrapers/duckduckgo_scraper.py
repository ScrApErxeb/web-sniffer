from typing import Any, Dict, List

from ddgs import DDGS

from .base_scraper import BaseScraper


class DuckDuckGoScraper(BaseScraper):
    def __init__(self, query: str, max_results: int = 10):
        super().__init__("DuckDuckGoScraper")
        self.query: str = query
        self.max_results: int = max_results

    def fetch_page(self, page: int = 0) -> List[Dict[str, Any]]:
        max_results = page * 10 + self.max_results
        with DDGS() as ddg:
            return list(ddg.text(self.query, max_results=max_results))

    def parse(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        seen_urls: set[str] = set()
        for item in items:
            title: str = item.get("title", "")
            url: str = item.get("href") or item.get("link", "")
            snippet: str = item.get("body", "")
            if title and url and url not in seen_urls:
                results.append({"title": title, "url": url, "snippet": snippet})
                seen_urls.add(url)
        return results

    def run(self, max_pages: int = 1) -> Dict[str, List[Dict[str, Any]]]:
        items = self.fetch_page()
        parsed = self.parse(items)
        return {self.query: parsed}
