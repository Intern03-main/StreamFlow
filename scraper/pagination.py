import time
from scraper.config import RETRY_ATTEMPTS, WAIT_TIME
from scraper.connection import is_connected, wait_for_connection


def safe_page_goto(page, url, retries=RETRY_ATTEMPTS, wait_time=WAIT_TIME):
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


import time
from scraper.config import BASE_URL
from scraper.connection import safe_page_goto

# def return_to_correct_page(page, scraper):
#     """Ensures the scraper returns to the correct page after reconnection."""
#     print(f"[INFO] Returning to page {scraper.current_page_number} after reconnection...")
#
#     # Reload base URL and return to correct page
#     safe_page_goto(page, BASE_URL)
#     time.sleep(3)
#
#     page_buttons = page.locator("a.paginate_button")
#     if page_buttons.count() == 0:
#         print("[ERROR] Pagination buttons not found after reload.")
#         return
#
#     # Get current page from DataTable using JS evaluation
#     current_page = page.evaluate("$('#tbstations').DataTable().page.info().page + 1")
#
#     if current_page == scraper.current_page_number:
#         print(f"[INFO] Already on the correct page {scraper.current_page_number}. No navigation needed.")
#         return
#
#     # Navigate to the correct page if needed
#     for _ in range(scraper.current_page_number - current_page):
#         next_button = page.locator("a.paginate_button.next:not(.disabled)")
#         if next_button.count() > 0:
#             print(f"[INFO] Navigating to page {scraper.current_page_number}...")
#             next_button.click()
#             page.wait_for_load_state("domcontentloaded")
#             time.sleep(3)
#
#             current_page = page.evaluate("$('#tbstations').DataTable().page.info().page + 1")
#             if current_page == scraper.current_page_number:
#                 print(f"[INFO] Successfully navigated to page {scraper.current_page_number}.")
#                 return
#         else:
#             print("[WARNING] Could not navigate to the expected page.")
#             break

def return_to_correct_page(page, scraper):
    """Ensures the scraper returns to the correct page after reconnection."""
    print(f"[INFO] Returning to page {scraper.current_page_number} after reconnection...")

    scraper.safe_page_goto(page, scraper.base_url)
    time.sleep(3)

    # Get total pages in DataTable
    total_pages = page.evaluate("$('#tbstations').DataTable().page.info().pages")

    # Get the current page
    current_page = page.evaluate("$('#tbstations').DataTable().page.info().page + 1")

    if current_page == scraper.current_page_number:
        print(f"[INFO] Already on the correct page {scraper.current_page_number}. No navigation needed.")
        return

    if scraper.current_page_number <= total_pages:
        # Jump directly to the correct page using DataTable API
        page.evaluate(f"$('#tbstations').DataTable().page({scraper.current_page_number - 1}).draw('page');")
        page.wait_for_load_state("domcontentloaded")
        print(f"[INFO] Successfully navigated to page {scraper.current_page_number}.")
    else:
        print(f"[ERROR] Requested page {scraper.current_page_number} exceeds available pages ({total_pages}).")



def click_next_page(page, scraper):
    """Clicks the 'Next' button to go to the next page."""
    next_button = page.locator("a.paginate_button.next:not(.disabled)")

    if next_button.count() > 0:
        if not is_connected():
            wait_for_connection(scraper.base_url, page)

        scraper.current_page_number += 1
        print(f"[INFO] Clicking 'Next' button to load page {scraper.current_page_number}...")
        next_button.click()
        page.wait_for_load_state("domcontentloaded")
        time.sleep(3)
        return True
    else:
        print("[INFO] No more pages available. Stopping the scraper.")
        return False