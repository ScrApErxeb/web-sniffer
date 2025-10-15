from typing import Any, Dict

from bs4 import BeautifulSoup

from core.http_client import fetch

from .base_scraper import BaseScraper


class WikipediaScraper(BaseScraper):
    def __init__(self, url: str):
        super().__init__("WikipediaScraper")
        self.url: str = url

    def fetch_page(self) -> str:
        return fetch(self.url)

    def parse(self, html: str) -> Dict[str, str]:
        soup = BeautifulSoup(html, "lxml")
        title: str = soup.title.string if soup.title else "No title"

        first_paragraph: str = ""
        content_div = soup.find("div", {"class": "mw-parser-output"})
        if content_div:
            for p in content_div.find_all("p"):
                text = p.get_text(strip=True)
                if text:
                    first_paragraph = text
                    break

        return {"title": title, "url": self.url, "snippet": first_paragraph}
