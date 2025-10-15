from scrapers.demo_scraper import DemoScraper


def test_parse_demo():
    html = "<html><head><title>Test Page</title></head><body></body></html>"
    scraper = DemoScraper()
    data = scraper.parse(html)
    assert data["title"] == "Test Page"
