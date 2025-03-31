import pandas as pd
from datetime import datetime


def save_to_excel(data):
    """Saves the scraped data to an Excel file."""
    if not data:
        print("[ERROR] No data to save.")
        return

    df = pd.DataFrame(data, columns=["Station ID", "Date", "Q (m³/s)"])
    filename = f"stream_daily-discharge_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    df.to_excel(filename, index=False)
    print(f"[INFO] Data saved to {filename}")
