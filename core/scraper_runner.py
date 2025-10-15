import logging
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Tuple

from core.cache import CacheInterface
from core.factory import ScraperFactory
from core.config import SCRAPER_RUNNER_CONFIG, HTTP_CONFIG

logger = logging.getLogger("ScraperRunner")
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")


class ScraperRunner:
    """
    Gère l'exécution parallèle des scrapers avec cache, retry, et rapport de performance.
    """

    SCRAPER_SOURCES = {
        "google": {"kwargs": {}, "max_retries": 2},
        "duckduckgo": {"kwargs": {"max_results": 20}, "max_retries": 2},
        "wikipedia": {"kwargs": {}, "max_retries": 1},
        "jeuneafrique": {"kwargs": {"pages": 2}, "max_retries": 2},
    }

    def __init__(self, countries: List[str], cache: CacheInterface):
        self.countries = countries
        self.cache = cache
        self.max_workers = SCRAPER_RUNNER_CONFIG["max_workers"]
        self.stats_perf: Dict[str, List[float]] = {}

    # -------------------------------
    # 🔁 Méthode générique avec retry
    # -------------------------------
    def _retry_operation(self, func, retries: int = 2, pause_range: Tuple[float, float] = None):
        pause_range = pause_range or HTTP_CONFIG["retry_pause_range"]
        for attempt in range(retries):
            try:
                return func()
            except Exception as e:
                wait_time = random.uniform(*pause_range)
                logger.warning(f"Tentative {attempt + 1} échouée ({e}). Retry dans {wait_time:.1f}s...")
                time.sleep(wait_time)
        raise RuntimeError("Toutes les tentatives ont échoué.")

    # -------------------------------
    # 🔍 Scraper un seul pays
    # -------------------------------
    def scrape_country(
        self, country: str
    ) -> Tuple[str, str, List[Dict[str, Any]], Dict[str, Dict[str, Any]]]:
        merged_results: List[Dict[str, Any]] = []
        stats: Dict[str, Dict[str, Any]] = {}

        logger.info(f"🌍 Scraping {country}...")

        for source, cfg in self.SCRAPER_SOURCES.items():
            kwargs = cfg.get("kwargs", {}).copy()
            retries = cfg.get("max_retries", 1)

            # Ajustements spécifiques
            if source == "wikipedia":
                kwargs["url"] = f"https://fr.wikipedia.org/wiki/{country.replace(' ', '_')}"
            elif source == "jeuneafrique":
                slug = country.lower().replace(" ", "-").replace("'", "")
                kwargs["slugs"] = [slug]

            start_time = time.time()
            data = self.cache.load(country, source)
            if data is not None:
                status = "CACHED"
            else:
                try:
                    def _run():
                        scraper = ScraperFactory.create(source, **kwargs)
                        if source == "duckduckgo":
                            fetched = scraper.fetch_page()
                            return scraper.parse(fetched)
                        elif source == "jeuneafrique":
                            return scraper.run().get(slug, [])
                        else:
                            return scraper.run()

                    data = self._retry_operation(_run, retries=retries)
                    self.cache.save(country, source, data)
                    status = "OK"
                except Exception as e:
                    logger.error(f"💥 Erreur {source} pour {country}: {e}")
                    data = []
                    status = "ERROR"
                    # Anti-429
                    time.sleep(random.uniform(*HTTP_CONFIG["anti_429_pause_range"]))

            elapsed = time.time() - start_time
            merged_results.extend(data)
            stats[source] = {"count": len(data), "status": status, "time_s": round(elapsed, 2)}
            self.stats_perf.setdefault(source, []).append(elapsed)

        logger.info(
            f"✅ {country} | total {len(merged_results)} résultats | stats: "
            + ", ".join([f"{k}:{v['status']}({v['count']})" for k, v in stats.items()])
        )

        return country, country, merged_results, stats

    # -------------------------------
    # 🚀 Lancer tous les scrapers
    # -------------------------------
    def run_all(
        self,
    ) -> List[Tuple[str, str, List[Dict[str, Any]], Dict[str, Dict[str, Any]]]]:
        results: List[Tuple[str, str, List[Dict[str, Any]], Dict[str, Dict[str, Any]]]] = []
        t0 = time.time()

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.scrape_country, c): c for c in self.countries}
            for future in as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as e:
                    logger.error(f"❌ Erreur globale sur {futures[future]}: {e}")

        total_time = round(time.time() - t0, 2)
        self._report_perf(total_time)
        return results

    # -------------------------------
    # 📊 Rapport de performance
    # -------------------------------
    def _report_perf(self, total_time: float):
        logger.info("📈 Rapport de performance:")
        for source, times in self.stats_perf.items():
            avg = sum(times) / len(times)
            logger.info(f"  - {source:12s} : {avg:.2f}s moyenne ({len(times)} appels)")
        logger.info(f"⏱️  Temps total : {total_time:.2f}s\n")


# -------------------------------
# 🔹 Lancer directement
# -------------------------------
if __name__ == "__main__":
    from core.cache import JSONCache

    countries_list = ["Burkina Faso", "Senegal", "Cote d'Ivoire", "Mali", "Niger"]
    cache = JSONCache(filepath="cache.json")

    runner = ScraperRunner(countries=countries_list, cache=cache)
    runner.run_all()
