import time
from datetime import datetime
import pandas as pd


def scrape_current_page(page, scraper):
    """Scrapes all year links available on the current page."""
    year_links = page.locator("a[href*='station_daily.aspx']")
    total_years = year_links.count()

    if total_years == 0:
        print("[ERROR] No year links found.")
        return
    print(f"[INFO] Found {total_years} year links. Scraping 20 available...")

    for i in range(total_years):  # Scrape all year links per page
        try:
            year_links = page.locator("a[href*='station_daily.aspx']")
            current_year_link = year_links.nth(i)

            print(f"\n[INFO] Clicking year link {i + 1}/{total_years}...")
            current_year_link.click()
            page.wait_for_load_state("domcontentloaded")
            time.sleep(3)

            scrape_data(page, scraper)

            # Return to correct page after scraping each year link
            from scraper.pagination import return_to_correct_page
            return_to_correct_page(page, scraper)

        except Exception as e:
            print(f"[ERROR] Failed to process year link {i + 1}: {e}")
            return_to_correct_page(page, scraper)


MAX_RETRIES = 3  # Number of times to wait for the table before reloading
MAX_RELOADS = 3  # Maximum times to reload the page


def scrape_data(page, scraper, reload_attempts=0):
    """Extracts data from the table while handling empty cells properly."""
    try:
        for attempt in range(MAX_RETRIES):
            table = page.locator("table.mystyle tbody")
            if table.count():
                break  # Table found, proceed with scraping
            print(f"[WARNING] Table not found. Retrying... ({attempt + 1}/{MAX_RETRIES})")
            time.sleep(2)  # Wait before retrying

        # If table still not found, reload the page
        table = page.locator("table.mystyle tbody")
        if not table.count():
            if reload_attempts < MAX_RELOADS:
                print(f"[ERROR] Table still not found. Reloading page... ({reload_attempts + 1}/{MAX_RELOADS})")
                page.reload()
                time.sleep(3)  # Wait for page to load
                return scrape_data(page, scraper, reload_attempts + 1)  # Retry after reload
            else:
                print("[CRITICAL] Table not found after multiple reloads. Manual intervention needed.")
                return  # Prevent infinite loop

        # Extract headers and month names
        rows = table.locator("tr")
        headers = rows.locator("th").all_text_contents()
        months = [h for h in headers if h not in ["Q", "Day"]]

        if not months:
            print("[ERROR] No valid headers found. Retrying...")
            return scrape_data(page, scraper, reload_attempts)

        # Extract station ID
        station_id_locator = page.locator("tr[valign='top'] td:has-text('STATION ID:') + td")
        station_id = station_id_locator.first.inner_text().strip() if station_id_locator.count() > 0 else "Unknown"
        print(f"[INFO] Station ID: {station_id}")

        # Extract year info for date parsing
        year_text_element = page.locator("div[style='text-align: center;'] b")
        year_text = year_text_element.first.inner_text().strip() if year_text_element.count() > 0 else None

        month_data = {month: {} for month in months}

        for row in rows.all():
            cells = row.locator("td")
            cell_texts = [cell.inner_text().strip() for cell in cells.all()]

            if not cell_texts or not cell_texts[0].isdigit():
                continue

            day = int(cell_texts[0])

            for i in range(len(months)):
                month_name = months[i]
                month_num = datetime.strptime(month_name, "%b").month
                value = cell_texts[i + 1] if i + 1 < len(cell_texts) else ""

                try:
                    value = float(value.replace(",", "").strip()) if value else None
                except ValueError:
                    value = None

                month_data[month_name][day] = value

        # Prepare current year link data
        current_data = []
        for month_name in months:
            month_num = datetime.strptime(month_name, "%b").month
            days_in_month = pd.Timestamp(f"{year_text}-{month_num:02}-01").days_in_month

            for day in range(1, days_in_month + 1):
                # Convert date to MySQL-compatible format
                date_str = f"{year_text}-{month_num:02}-{day:02}"
                value = month_data[month_name].get(day, "")
                current_data.append([station_id, date_str, value])

        # Add the current year link data to main scraper data
        scraper.data.extend(current_data)

    except Exception as e:
        print(f"[ERROR] Failed to scrape data: {e}")