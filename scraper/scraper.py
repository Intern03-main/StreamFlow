from scraper.config import BASE_URL
from scraper.connection import wait_for_connection
from scraper.pagination import return_to_correct_page, click_next_page
from scraper.data_processing import scrape_current_page
from scraper.utils import save_to_excel
from scraper.db_connection import create_table, insert_data

from playwright.sync_api import sync_playwright
import time


class TableScraper:
    def __init__(self, headless=True):
        self.base_url = BASE_URL
        self.data = []
        self.headless = headless
        self.current_page_number = 1

    def run(self):
        """Main function to start the scraper and handle pagination."""
        # Create table before starting the scraper
        create_table()

        with sync_playwright() as p:
            print("[INFO] Launching browser...")
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()

            wait_for_connection(self.base_url, page)
            self.safe_page_goto(page, self.base_url)
            return_to_correct_page(page, self)  # Use correct page handling

            while True:
                try:
                    scrape_current_page(page, self)  # Pass self for data updates
                    if not click_next_page(page, self):
                        break
                except Exception as e:
                    print(f"[ERROR] An error occurred: {e}")
                    wait_for_connection(self.base_url, page)
                    return_to_correct_page(page, self)

            browser.close()

        # Save data to Excel
        save_to_excel(self.data)

        # Insert scraped data into MySQL database
        if self.data:
            insert_data(self.data)
        else:
            print("[WARNING] No data to insert into MySQL database.")

    def safe_page_goto(self, page, url, retries=5, wait_time=10):
        """Attempts to load a page with retries if internet fails."""
        attempt = 0
        while attempt < retries:
            try:
                print(f"[INFO] Loading {url}... (Attempt {attempt + 1}/{retries})")
                page.goto(url, timeout=30000, wait_until="domcontentloaded")
                page.wait_for_load_state("load")
                time.sleep(3)
                return
            except Exception as e:
                print(f"[WARNING] Failed to load page: {e}")
                attempt += 1
                time.sleep(wait_time)

        print("[ERROR] All attempts to load the page failed. Exiting...")
        raise Exception("Failed to load page after multiple retries.")
