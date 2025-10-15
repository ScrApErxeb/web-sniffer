from typing import Any
from scrapers.google_search_scraper import GoogleSearchScraper
from scrapers.duckduckgo_scraper import DuckDuckGoScraper
from scrapers.wikipedia_scraper import WikipediaScraper
from scrapers.jeune_afrique_scraper import JeuneAfriqueMultiCountryScraper


class ScraperFactory:
    """
    Fabrique les instances de scraper selon le nom de la source.
    """

    @staticmethod
    def create(source: str, **kwargs) -> Any:
        source = source.lower()
        if source == "google":
            query = kwargs.get("query")
            if not query:
                raise ValueError("GoogleSearchScraper requires 'query'")
            return GoogleSearchScraper(query=query, **kwargs)

        elif source == "duckduckgo":
            query = kwargs.get("query")
            if not query:
                raise ValueError("DuckDuckGoScraper requires 'query'")
            return DuckDuckGoScraper(query=query, **kwargs)

        elif source == "wikipedia":
            url = kwargs.get("url")
            if not url:
                raise ValueError("WikipediaScraper requires 'url'")
            return WikipediaScraper(url=url)

        elif source == "jeuneafrique":
            slugs = kwargs.get("slugs")
            pages = kwargs.get("pages", 1)
            if not slugs:
                raise ValueError("JeuneAfriqueMultiCountryScraper requires 'slugs'")
            return JeuneAfriqueMultiCountryScraper(slugs=slugs, pages=pages)

        else:
            raise ValueError(f"Source inconnue pour le ScraperFactory: {source}")
