from unittest.mock import Mock, patch

import pytest

from scrapers.jeune_afrique_scraper import JeuneAfriqueMultiCountryScraper

html_page = """
<html>
<body>
<article><a href="/pays/burkina-faso/article1">Title1</a></article>
<article><a href="/pays/burkina-faso/article2">Title2</a></article>
</body>
</html>
"""

@patch("requests.get")
def test_jeune_afrique_scraper(mock_get):
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.text = html_page
    mock_get.return_value = mock_resp

    scraper = JeuneAfriqueMultiCountryScraper(slugs=["burkina-faso"], pages=1)
    results = scraper.run()
    
    assert "burkina-faso" in results
    assert len(results["burkina-faso"]) == 2
    assert results["burkina-faso"][0]["title"] == "Title1"
    assert results["burkina-faso"][0]["url"] == "https://www.jeuneafrique.com/pays/burkina-faso/article1"
