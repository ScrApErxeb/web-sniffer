import pytest
from unittest.mock import MagicMock
from multi_scrap import run_all
from unittest.mock import patch


class DummyCache:
    def __init__(self):
        self.storage = {}

    def save(self, query, source, results):
        self.storage[(query, source)] = results

    def load(self, query, source):
        return self.storage.get((query, source))

def test_run_all():
    mock_cache = DummyCache()
    countries = ["testland"]

    with patch("scrapers.google_search_scraper.GoogleSearchScraper.run", return_value={"testland": [{"title": "dummy", "url": "http://example.com", "snippet": "text"}]}), \
         patch("scrapers.duckduckgo_scraper.DuckDuckGoScraper.run", return_value={"testland": [{"title": "dummy", "url": "http://example.com", "snippet": "text"}]}), \
         patch("scrapers.jeune_afrique_scraper.JeuneAfriqueMultiCountryScraper.run", return_value={"testland": [{"title": "dummy", "url": "http://example.com", "snippet": "text"}]}):
        
        results = run_all(countries=countries, cache_instance=mock_cache)

        for country, query, merged_results, stats in results:
            for source in stats:
                cached = mock_cache.load(query, source)
                assert cached is not None
