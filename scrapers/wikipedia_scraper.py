from bs4 import BeautifulSoup
from .base_scraper import BaseScraper
from core.logger import logger

class WikipediaScraper(BaseScraper):
    def __init__(self):
        super().__init__("WikipediaScraper")

    def parse(self, html: str) -> dict:
        soup = BeautifulSoup(html, "lxml")
        title = soup.title.string if soup.title else "No title"

        first_paragraph = "No content"
        content_div = soup.find("div", {"class": "mw-parser-output"})
        if content_div:
            # Chercher le premier <p> non vide
            for p in content_div.find_all("p"):
                text = p.get_text(strip=True)
                if text:
                    first_paragraph = text
                    break

        return {
            "title": title,
            "first_paragraph": first_paragraph
        }
