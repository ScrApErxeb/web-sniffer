import pytest
from unittest.mock import patch
from scrapers.google_search_scraper import GoogleSearchScraper
import json

def test_google_scraper():
    mock_data = {
        "items": [
            {"title": "t1", "link": "url1", "snippet": "s1"},
            {"title": "t2", "link": "url2", "snippet": "s2"}
        ]
    }

    scraper = GoogleSearchScraper(query="test")

    # Patch fetch_page pour renvoyer un JSON string
    with patch.object(scraper, "fetch_page", return_value=json.dumps(mock_data)):
        results = scraper.run(max_pages=1)

    assert "test" in results
    assert results["test"][0]["title"] == "t1"
    assert results["test"][0]["url"] == "url1"
    assert results["test"][0]["snippet"] == "s1"
