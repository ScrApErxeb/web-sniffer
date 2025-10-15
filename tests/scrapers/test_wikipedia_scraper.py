import pytest
from unittest.mock import patch
from scrapers.wikipedia_scraper import WikipediaScraper

def test_wikipedia_scraper():
    scraper = WikipediaScraper("https://fr.wikipedia.org/wiki/Python")

    # Patch de la méthode fetch_page pour renvoyer un HTML simulé
    with patch.object(scraper, "fetch_page", return_value="""
        <html>
            <head><title>Python</title></head>
            <body>
                <div class="mw-parser-output">
                    <p>Python est un langage de programmation.</p>
                </div>
            </body>
        </html>
    """):
        html = scraper.fetch_page()
        data = scraper.parse(html)

    assert isinstance(data, dict)
    assert data["title"] == "Python"
    assert data["snippet"].startswith("Python est un langage")
