from scrapers.jeune_afrique_scraper import JeuneAfriqueCountryScraper
from core.storage import save_data

if __name__ == "__main__":
    scraper = JeuneAfriqueCountryScraper(slug="burkina-faso", pages=2)
    data = scraper.run()
    save_data("JeuneAfrique-BurkinaFaso", data)
    print(f"Scraping terminé : {len(data['articles'])} articles récupérés.")
