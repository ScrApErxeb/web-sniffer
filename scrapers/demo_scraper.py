from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class DemoScraper(BaseScraper):
    def __init__(self):
        super().__init__("DemoScraper")

    def parse(self, html: str) -> dict:
        soup = BeautifulSoup(html, "lxml")
        title = soup.title.string if soup.title else "No title"
        return {"title": title}
