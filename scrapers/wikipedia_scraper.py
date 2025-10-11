from bs4 import BeautifulSoup
from .base_scraper import BaseScraper
from core.logger import logger

class WikipediaScraper(BaseScraper):
    def __init__(self, url: str = None):
        super().__init__("WikipediaScraper")
        self.url = url

    def parse(self, html: str) -> dict:
        soup = BeautifulSoup(html, "lxml")
        title = soup.title.string if soup.title else "No title"

        first_paragraph = ""
        content_div = soup.find("div", {"class": "mw-parser-output"})
        if content_div:
            for p in content_div.find_all("p"):
                text = p.get_text(strip=True)
                if text:
                    first_paragraph = text
                    break

        return {
            "title": title,
            "url": self.url or "",
            "snippet": first_paragraph
        }
