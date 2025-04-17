Streamflow Data Scraper - README

Description
This project scrapes daily streamflow data from the DPWH's "Streamflow Management System" website using Playwright. The collected data includes station information (STATION ID), Date, and Streamflow or Discharge readings (Q). The data is saved in CSV format and inserted into a MySQL database.

Columns

| Column         | Description                                                   |
|----------------|---------------------------------------------------------------|
| Station ID     | Unique station code of Rivers                                 |
| Date           | Date when a specific daily streamflow rate recorded           |
| Q              | The discharge or streamflow rate at a specific time           |

Notes
- Data is scraped per year links available in a page and paginated automatically.
