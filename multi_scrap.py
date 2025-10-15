# multi_scrap.py
import logging
from time import sleep
from urllib.parse import quote

from core.cache import JSONCache
from core.logger import logger
from scrapers.google_search_scraper import GoogleSearchScraper
from scrapers.duckduckgo_scraper import DuckDuckGoScraper
from scrapers.wikipedia_scraper import WikipediaScraper
from scrapers.jeune_afrique_scraper import JeuneAfriqueMultiCountryScraper

# Liste des pays et leurs slugs corrects pour JeuneAfrique
COUNTRIES = {
    "Burkina Faso": {"wiki": "Burkina_Faso", "ja_slug": "burkina-faso"},
    "Senegal": {"wiki": "Senegal", "ja_slug": "senegal"},
    "Cote d'Ivoire": {"wiki": "Côte_d'Ivoire", "ja_slug": "cote-divoire"},
    # Ajouter d'autres pays ici
}

cache = JSONCache("cache.json")

def scrape_country(country_name: str, slugs: dict, max_pages: int = 2):
    logger.info(f"Scraping {country_name}...")

    stats = {}
    merged_results = []

    # --- Google ---
    google_scraper = GoogleSearchScraper(query=country_name)
    try:
        results = google_scraper.run(max_pages=1)
        merged_results.extend(results[country_name])
        stats["google"] = {"count": len(results[country_name]), "status": "OK"}
        cache.save(country_name, "google", results[country_name])
    except Exception as e:
        logger.error(f"Erreur Google pour {country_name}: {e}")
        stats["google"] = {"count": 0, "status": "ERROR"}

    sleep(1)  # anti-throttle

    # --- DuckDuckGo ---
    ddg_scraper = DuckDuckGoScraper(query=country_name, max_results=20)
    try:
        results = ddg_scraper.run(max_pages=1)
        merged_results.extend(results[country_name])
        stats["duckduckgo"] = {"count": len(results[country_name]), "status": "OK"}
        cache.save(country_name, "duckduckgo", results[country_name])
    except Exception as e:
        logger.error(f"Erreur DuckDuckGo pour {country_name}: {e}")
        stats["duckduckgo"] = {"count": 0, "status": "ERROR"}

    sleep(1)

    # --- Wikipedia ---
    wiki_url = f"https://fr.wikipedia.org/wiki/{quote(slugs['wiki'])}"
    wiki_scraper = WikipediaScraper(url=wiki_url)
    try:
        html = wiki_scraper.fetch_page()  # utilise fetch_page si implémenté
        data = wiki_scraper.parse(html)
        merged_results.append(data)
        stats["wikipedia"] = {"count": 1, "status": "OK"}
        cache.save(country_name, "wikipedia", data)
    except Exception as e:
        logger.error(f"Erreur Wikipedia pour {country_name}: {e}")
        stats["wikipedia"] = {"count": 0, "status": "ERROR"}

    sleep(1)

    # --- Jeune Afrique ---
    ja_scraper = JeuneAfriqueMultiCountryScraper(slugs=[slugs["ja_slug"]], pages=max_pages)
    try:
        results = ja_scraper.run()
        country_articles = results.get(slugs["ja_slug"], [])
        merged_results.extend(country_articles)
        stats["jeuneafrique"] = {"count": len(country_articles), "status": "OK"}
        cache.save(country_name, "jeuneafrique", country_articles)
    except Exception as e:
        logger.error(f"Erreur JeuneAfrique pour {country_name}: {e}")
        stats["jeuneafrique"] = {"count": 0, "status": "ERROR"}

    logger.info(f"{country_name} | fusionné {len(merged_results)} | stats: {stats}")
    return country_name, merged_results, stats

def run_all(countries: dict = COUNTRIES, max_pages: int = 2):
    results = []
    for country_name, slugs in countries.items():
        try:
            result = scrape_country(country_name, slugs, max_pages=max_pages)
            results.append(result)
        except Exception as e:
            logger.error(f"Erreur globale pour {country_name}: {e}")
    return results

if __name__ == "__main__":
    run_all()
