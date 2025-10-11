from bs4 import BeautifulSoup
import requests
from .base_scraper import BaseScraper

class SearchScraper(BaseScraper):
    """
    Scraper générique pour moteurs HTML : DuckDuckGo et Bing (Google API séparé)
    """
    def __init__(self, query: str, engine: str = "duckduckgo"):
        super().__init__(name=f"SearchScraper-{engine}")
        self.query = query
        self.engine = engine.lower()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (compatible; WebSniffer/1.0)"
        }

    def fetch(self, page: int = 0):
        offset = page * 10
        if self.engine == "duckduckgo":
            url = f"https://duckduckgo.com/html/?q={self.query}&s={offset}"
        elif self.engine == "bing":
            url = f"https://www.bing.com/search?q={self.query}&first={offset + 1}"
        elif self.engine == "google":
            url = f"https://www.google.com/search?q={self.query}&start={offset}"
        else:
            raise ValueError(f"Moteur inconnu: {self.engine}")

        resp = requests.get(url, headers=self.headers, timeout=10)
        resp.raise_for_status()
        return resp.text

    def parse(self, html):
        soup = BeautifulSoup(html, "html.parser")
        results = []

        if self.engine == "duckduckgo":
            for res in soup.select(".result__a"):
                title = res.get_text(strip=True)
                url = res.get("href")
                if title and url:
                    results.append({"title": title, "url": url})
        elif self.engine == "bing":
            for h2 in soup.select("li.b_algo h2 a"):
                title = h2.get_text(strip=True)
                url = h2.get("href")
                if title and url:
                    results.append({"title": title, "url": url})
        elif self.engine == "google":
            for a in soup.select("a h3"):
                title = a.get_text(strip=True)
                parent = a.find_parent("a")
                url = parent.get("href") if parent else None
                if title and url:
                    results.append({"title": title, "url": url})

        return results

    def run(self, max_pages: int = 1):
        all_results = []
        for page in range(max_pages):
            html = self.fetch(page=page)
            results = self.parse(html)
            if not results:
                break
            all_results.extend(results)
        return {self.query: all_results}
