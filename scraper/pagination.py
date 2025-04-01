import time
from scraper.connection import is_connected, wait_for_connection


def safe_page_goto(page, url, wait_time=10):
    """Attempts to load a page and waits indefinitely until it succeeds."""
    attempt = 1
    while True:
        try:
            print(f"[INFO] Loading {url}... (Attempt {attempt})")
            page.goto(url, timeout=60000, wait_until="load")  # Set longer timeout (60s)
            page.wait_for_load_state("networkidle")  # Wait until all network requests are done
            print("[INFO] Page loaded successfully!")
            return  # Exit loop once successful
        except Exception as e:
            print(f"[WARNING] Failed to load page: {e}")
            print(f"[INFO] Retrying in {wait_time} seconds...")
            time.sleep(wait_time)  # Wait before retrying
            attempt += 1  # Increment attempt count



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