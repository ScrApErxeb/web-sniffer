import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class JeuneAfriqueMultiCountryScraper(BaseScraper):
    def __init__(self, slugs: list = None, pages: int = 2):
        if slugs is None:
            slugs = ["burkina-faso", "cote-d-ivoire", "senegal"]
        super().__init__(name="JeuneAfrique-MultiCountry")
        self.slugs = slugs
        self.pages = pages
        self.base_domain = "https://www.jeuneafrique.com"

    def fetch(self, slug: str, page: int = 1):
        url = f"{self.base_domain}/pays/{slug}/page/{page}/" if page > 1 else f"{self.base_domain}/pays/{slug}/"
        resp = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (compatible; ScraperBot/1.0)"
        })
        resp.raise_for_status()
        return resp.text

    def parse(self, html: str):
        soup = BeautifulSoup(html, "html.parser")
        articles = []
        for a in soup.select("article a"):
            title = a.get_text(strip=True)
            url = a.get("href")
            if title and url:
                if url.startswith("/"):
                    url = f"{self.base_domain}{url}"
                articles.append({
                    "title": title,
                    "url": url,
                    "snippet": ""  # snippet vide pour uniformité
                })
        return articles

    def run(self):
        all_articles = {}
        for slug in self.slugs:
            country_articles = []
            for page in range(1, self.pages + 1):
                html = self.fetch(slug, page)
                articles = self.parse(html)
                country_articles.extend(articles)
            all_articles[slug] = country_articles
        return all_articles
