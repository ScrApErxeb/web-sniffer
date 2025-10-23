# multi_scrap.py
import logging
from typing import Any, Dict, List, Tuple

from core.cache import CacheInterface, JSONCache
from core.factory import ScraperFactory

logger = logging.getLogger("multi_scrap")
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

# mapping pays → sources (scraper name et paramètres)
SCRAPER_SOURCES = {
    "google": {"name": "google", "kwargs": {}},
    "duckduckgo": {"name": "duckduckgo", "kwargs": {"max_results": 20}},
    "wikipedia": {"name": "wikipedia", "kwargs": {}},
    "jeuneafrique": {"name": "jeuneafrique", "kwargs": {"pages": 2}},
}

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

        for source, cfg in SCRAPER_SOURCES.items():
            scraper_name = cfg["name"]
            kwargs = cfg.get("kwargs", {}).copy()

            # ajustements spécifiques
            if scraper_name == "wikipedia":
                kwargs["url"] = f"https://fr.wikipedia.org/wiki/{country.replace(' ', '_')}"
            elif scraper_name == "jeuneafrique":
                slug = country.lower().replace(" ", "-").replace("'", "")
                kwargs["slugs"] = [slug]

            # load from cache
            data = cache_instance.load(country, source)
            if data is not None:
                status = "CACHED"
            else:
                try:
                    scraper = ScraperFactory.create(scraper_name, **kwargs)
                    if scraper_name in ["duckduckgo"]:
                        # fetch + parse séparé
                        fetched = scraper.fetch_page()  # ou fetch() selon le scraper
                        data = scraper.parse(fetched)
                    else:
                        # run() standard
                        data = scraper.run()
                        # pour JeuneAfrique, récupérer le contenu du slug
                        if scraper_name == "jeuneafrique":
                            data = data.get(slug, [])
                    cache_instance.save(country, source, data)
                    status = "OK"
                except Exception as e:
                    logger.error(f"Erreur {scraper_name} pour {country}: {e}")
                    data = []
                    status = "ERROR"

            merged_results.extend(data)
            stats[source] = {"count": len(data), "status": status}

        logger.info(f"{country} | fusionné {len(merged_results)} | stats: {stats}")
        results.append((country, country, merged_results, stats))

    return results


if __name__ == "__main__":
    countries_list = ["Burkina Faso", "Senegal", "Cote d'Ivoire"]
    cache = JSONCache(filepath="cache.json")
    run_all(countries_list, cache)
