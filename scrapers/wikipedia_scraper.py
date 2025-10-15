from typing import Any, Dict
from bs4 import BeautifulSoup
from core.http_client import fetch
from .base_scraper import BaseScraper


class WikipediaScraper(BaseScraper):
    def __init__(self, url: str | None = None):
        super().__init__("WikipediaScraper")
        self.url: str = url or "https://fr.wikipedia.org/wiki/Main_Page"

    def fetch_page(self, page: str | None = None) -> str:
        """
        Récupère le HTML d'une page Wikipedia.
        :param page: slug de la page (ex: 'Burkina_Faso')
        """
        target_url = f"https://fr.wikipedia.org/wiki/{page}" if page else self.url
        return fetch(target_url)

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

    def run(self) -> list[dict[str, str]]:
        """
        Scrape complet d'une page Wikipedia.
        """
        slug = self.url.split("/")[-1]
        html = self.fetch_page(page=slug)
        data = self.parse(html)
        return [data]
