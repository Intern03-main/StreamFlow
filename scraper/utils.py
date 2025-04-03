import os
import pandas as pd
from datetime import datetime


def save_to_excel(data):
    """Saves the scraped data to an Excel file in the 'Daily_Discharge_Files' directory."""
    if not data:
        print("[ERROR] No data to save.")
        return

    # Create the directory if it doesn't exist
    output_dir = "Daily_Discharge_Files"
    os.makedirs(output_dir, exist_ok=True)

    # Generate the file path
    filename = f"stream_daily-discharge_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    filepath = os.path.join(output_dir, filename)

    # Save the data
    df = pd.DataFrame(data, columns=["Station ID", "Date", "Q (m³/s)"])
    df.to_excel(filepath, index=False)

    print(f"[INFO] Data saved to {filepath}")
