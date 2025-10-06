import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class JeuneAfriqueCountryScraper(BaseScraper):
    def __init__(self, slug: str = "burkina-faso", pages: int = 2):
        super().__init__(name=f"JeuneAfrique-{slug}")
        self.slug = slug
        self.pages = pages
        self.base_url = f"https://www.jeuneafrique.com/pays/{slug}/"

    def fetch(self, page: int = 1):
        url = f"{self.base_url}page/{page}/" if page > 1 else self.base_url
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
                articles.append({"title": title, "url": url})
        return articles

    def run(self):
        all_articles = []
        for page in range(1, self.pages + 1):
            html = self.fetch(page)
            articles = self.parse(html)
            all_articles.extend(articles)
        return {"articles": all_articles}
