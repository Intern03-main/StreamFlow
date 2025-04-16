import os
import pandas as pd
from datetime import datetime

last_successful_index = 0
last_failed_index = None

cache = {}


def save_to_csv(data):
    """Saves the scraped data to a CSV file in the 'Daily_Discharge_Files' directory."""
    if not data:
        print("[ERROR] No data to save.")
        return

    # Save to a CSV file
    output_dir = os.path.join(os.path.expanduser("~"), "Desktop", "Daily_Discharge_Files")
    os.makedirs(output_dir, exist_ok=True)

    # Generate the file path
    filename = f"stream_daily-discharge_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    filepath = os.path.join(output_dir, filename)

    # Save the data
    df = pd.DataFrame(data, columns=["Station ID", "Date", "Q"])
    df.to_csv(filepath, index=False)

    print(f"[INFO] Data saved to {filepath}")
