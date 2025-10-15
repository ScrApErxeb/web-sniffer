# multi_scrap.py
import logging
from typing import Any, Dict, List, Tuple

from core.cache import CacheInterface, JSONCache
from scrapers.duckduckgo_scraper import DuckDuckGoScraper
from scrapers.google_search_scraper import GoogleSearchScraper
from scrapers.jeune_afrique_scraper import JeuneAfriqueMultiCountryScraper
from scrapers.wikipedia_scraper import WikipediaScraper

logger = logging.getLogger("multi_scrap")
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")


def run_all(
    countries: List[str],
    cache_instance: CacheInterface
) -> List[Tuple[str, str, List[Dict[str, Any]], Dict[str, Dict[str, Any]]]]:
    """
    Scrape toutes les sources pour chaque pays, avec cache et stats.
    
    Returns:
        List of tuples: (country, query, merged_results, stats)
    """
    results: List[Tuple[str, str, List[Dict[str, Any]], Dict[str, Dict[str, Any]]]] = []

    for country in countries:
        logger.info(f"Scraping {country}...")

        merged_results: List[Dict[str, Any]] = []
        stats: Dict[str, Dict[str, Any]] = {}

        # --- Google ---
        google_scraper = GoogleSearchScraper(query=country)
        google_data = cache_instance.load(country, "google")
        if google_data is None:
            try:
                google_data = google_scraper.run(max_pages=2)["Burkina Faso"]
                cache_instance.save(country, "google", google_data)
                status = "OK"
            except Exception as e:
                logger.error(f"Erreur Google pour {country}: {e}")
                google_data = []
                status = "ERROR"
        else:
            status = "CACHED"
        merged_results.extend(google_data)
        stats["google"] = {"count": len(google_data), "status": status}

        # --- DuckDuckGo ---
        ddg_scraper = DuckDuckGoScraper(query=country, max_results=20)
        ddg_data = cache_instance.load(country, "duckduckgo")
        if ddg_data is None:
            try:
                items = ddg_scraper.fetch_page()
                ddg_data = ddg_scraper.parse(items)
                cache_instance.save(country, "duckduckgo", ddg_data)
                status = "OK"
            except Exception as e:
                logger.error(f"Erreur DuckDuckGo pour {country}: {e}")
                ddg_data = []
                status = "ERROR"
        else:
            status = "CACHED"
        merged_results.extend(ddg_data)
        stats["duckduckgo"] = {"count": len(ddg_data), "status": status}

        # --- Wikipedia ---
        wiki_url = f"https://fr.wikipedia.org/wiki/{country.replace(' ', '_')}"
        wiki_scraper = WikipediaScraper(url=wiki_url)
        wiki_data = cache_instance.load(country, "wikipedia")
        if wiki_data is None:
            try:
                html = wiki_scraper.fetch_page()
                wiki_data = [wiki_scraper.parse(html)]
                cache_instance.save(country, "wikipedia", wiki_data)
                status = "OK"
            except Exception as e:
                logger.error(f"Erreur Wikipedia pour {country}: {e}")
                wiki_data = []
                status = "ERROR"
        else:
            status = "CACHED"
        merged_results.extend(wiki_data)
        stats["wikipedia"] = {"count": len(wiki_data), "status": status}

        # --- Jeune Afrique ---
        # convertir les noms pays en slugs corrects
        slug = country.lower().replace(" ", "-").replace("'", "")
        ja_scraper = JeuneAfriqueMultiCountryScraper(slugs=[slug], pages=2)
        ja_data = cache_instance.load(country, "jeuneafrique")
        if ja_data is None:
            try:
                ja_data_dict = ja_scraper.run()
                ja_data = ja_data_dict.get(slug, [])
                cache_instance.save(country, "jeuneafrique", ja_data)
                status = "OK"
            except Exception as e:
                logger.error(f"Erreur JeuneAfrique pour {country}: {e}")
                ja_data = []
                status = "ERROR"
        else:
            status = "CACHED"
        merged_results.extend(ja_data)
        stats["jeuneafrique"] = {"count": len(ja_data), "status": status}

        logger.info(f"{country} | fusionné {len(merged_results)} | stats: {stats}")

        results.append((country, country, merged_results, stats))

    return results


if __name__ == "__main__":
    countries_list = ["Burkina Faso", "Senegal", "Cote d'Ivoire"]
    cache = JSONCache(filepath="cache.json")
    run_all(countries_list, cache)
