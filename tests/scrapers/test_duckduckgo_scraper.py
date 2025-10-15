from unittest.mock import MagicMock, patch

from scrapers.duckduckgo_scraper import DuckDuckGoScraper


@patch("scrapers.duckduckgo_scraper.DDGS")
def test_duckduckgo_scraper(mock_ddgs_class):
    mock_ddgs = MagicMock()
    mock_ddgs.text.return_value = [
        {"title": "Title1", "href": "https://url1.com", "body": "Snippet1"}
    ]
    mock_ddgs_class.return_value.__enter__.return_value = mock_ddgs

    scraper = DuckDuckGoScraper(query="test", max_results=10)
    results = scraper.run(max_pages=1)
    
    assert "test" in results
    assert results["test"][0]["title"] == "Title1"
    assert results["test"][0]["url"] == "https://url1.com"
    assert results["test"][0]["snippet"] == "Snippet1"
