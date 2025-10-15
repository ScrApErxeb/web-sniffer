from typing import Any, Dict, List

import requests
from bs4 import BeautifulSoup

from .base_scraper import BaseScraper


class JeuneAfriqueMultiCountryScraper(BaseScraper):
    def __init__(self, slugs: List[str], pages: int = 2):
        super().__init__("JeuneAfriqueMultiCountryScraper")
        self.slugs: List[str] = slugs
        self.pages: int = pages
        self.base_domain: str = "https://www.jeuneafrique.com"

    def fetch_page(self, slug: str, page: int = 1) -> str:
        url: str = f"{self.base_domain}/pays/{slug}/page/{page}/" if page > 1 else f"{self.base_domain}/pays/{slug}/"
        resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        return resp.text

    def parse(self, html: str) -> List[Dict[str, str]]:
        soup = BeautifulSoup(html, "html.parser")
        articles: List[Dict[str, str]] = []
        for a in soup.select("article a"):
            title = a.get_text(strip=True)
            url = a.get("href", "")
            if url.startswith("/"):
                url = f"{self.base_domain}{url}"
            if title and url:
                articles.append({"title": title, "url": url, "snippet": ""})
        return articles

    def run(self) -> Dict[str, List[Dict[str, str]]]:
        all_articles: Dict[str, List[Dict[str, str]]] = {}
        for slug in self.slugs:
            country_articles: List[Dict[str, str]] = []
            for page in range(1, self.pages + 1):
                html = self.fetch_page(slug, page)
                country_articles.extend(self.parse(html))
            all_articles[slug] = country_articles
        return all_articles
