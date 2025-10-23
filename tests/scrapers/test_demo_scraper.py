from scrapers.demo_scraper import DemoScraper

html_demo = """
<html>
<head><title>Demo Page</title></head>
<body>
<p>Some content</p>
</body>
</html>
"""

def test_demo_scraper_parse():
    scraper = DemoScraper()
    data = scraper.parse(html_demo)

    assert data["title"] == "Demo Page"
