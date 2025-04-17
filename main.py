from scraper.scraper import TableScraper

if __name__ == "__main__":
    scraper = TableScraper(headless=False)
    scraper.run()