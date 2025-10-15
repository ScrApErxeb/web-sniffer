from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class WikipediaScraper(BaseScraper):
    def __init__(self, url: str = None):
        super().__init__("WikipediaScraper")
        self.url = url

    def fetch_page(self):
        import requests
        if not self.url:
            raise ValueError("URL non définie pour WikipediaScraper")
        resp = requests.get(self.url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        return resp.text

    # ✅ Implémentation réelle pour lever l’abstraction
    def parse(self, html: str):
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

    def run(self):
        html = self.fetch_page()
        return {self.url: self.parse(html)}
