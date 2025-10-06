from scrapers.demo_scraper import DemoScraper

if __name__ == "__main__":
    scraper = DemoScraper()
    scraper.start("https://httpbin.org/html")
