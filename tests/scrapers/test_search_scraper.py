from unittest.mock import Mock, patch

import pytest

from scrapers.search_scraper import SearchScraper

html_ddg = '<a class="result__a" href="https://example.com">Test Title</a>'
html_bing = '<li class="b_algo"><h2><a href="https://example.com">Test Title</a></h2></li>'
html_google = '<a href="https://example.com"><h3>Test Title</h3></a>'

@patch("requests.get")
def test_search_scraper_duckduckgo(mock_get):
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.text = html_ddg
    mock_get.return_value = mock_resp

    scraper = SearchScraper(query="test", engine="duckduckgo")
    results = scraper.run(max_pages=1)
    assert results["test"][0]["title"] == "Test Title"
    assert results["test"][0]["url"] == "https://example.com"

@patch("requests.get")
def test_search_scraper_bing(mock_get):
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.text = html_bing
    mock_get.return_value = mock_resp

    scraper = SearchScraper(query="test", engine="bing")
    results = scraper.run(max_pages=1)
    assert results["test"][0]["title"] == "Test Title"

@patch("requests.get")
def test_search_scraper_google(mock_get):
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.text = html_google
    mock_get.return_value = mock_resp

    scraper = SearchScraper(query="test", engine="google")
    results = scraper.run(max_pages=1)
    assert results["test"][0]["title"] == "Test Title"
