
# Streamflow Data Scraper

This project is a web scraper built using **Playwright** in Python. It extracts **daily streamflow data** from DPWH's website (Streamflow Management System).

---

## Features

### Resilient Internet Handling
- Waits indefinitely if the internet disconnects.
- Automatically retries page loads.
- Returns to the correct pagination page after reconnection.

### Streamflow Data Scraping
- Extracts daily streamflow values across months.
- Automatically calculates missing entries using forward imputation (to be integrated).
- Converts scraped values into MySQL-compatible format.

### Pagination Support
- Scrapes all year links per page and moves to the next page.
- Skips already-processed links using an in-memory cache.

### MySQL Integration
- Automatically creates, drops, and inserts into the database.
- Stores all extracted data for further analysis.

---

## Setup & Usage

1. Install dependencies:
```bash
pip install -r requirements.txt
playwright install
```
2. Make sure that the .env file contents match the MySQL database credentials you're using.
   
3. Run the scraper:
```py
python main.py
```

---

## Station Names and its Coordinates(Latitude/Longhitude) GDrive Link
```bash
https://docs.google.com/spreadsheets/d/1wP71_bU1YieCch77IrSiCY3lSf1OI5j6/edit?usp=sharing&ouid=100929269929134209125&rtpof=true&sd=true
```


---

## Columns in the stored .csv file

| Column         | Description                                                   |
|----------------|---------------------------------------------------------------|
| Station ID     | Unique station code of Rivers                                 |
| Date           | Date when a specific daily streamflow rate recorded           |
| Q              | The discharge or streamflow rate at a specific time           |

## File Output:

- The cleaned data is saved as:  
  **`stream_daily-discharge_<timestamp>.csv`**  
  Located in:  
  **Desktop/Daily_Discharge_Files/**

## Example Output (MySQL Format)

| station_id | date       | discharge|
|------------|------------|----------|
| CAR.001    | 2005-01-18 | 31500    |
| R06.010    | 1992-01-31 | 2880     |
| R08.A001   | 1993-11-01 | 15440    |

---
