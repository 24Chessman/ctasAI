# merge_buoy_cyclones.py
import pandas as pd
from datetime import datetime

# Load datasets
buoy = pd.read_csv("buoy.csv", parse_dates=["date"])
cyclones = pd.read_csv("cyclones.csv")

# Ensure cyclone date columns are datetime
cyclones["start_date"] = pd.to_datetime(cyclones["start_date"], errors="coerce")
cyclones["end_date"] = pd.to_datetime(cyclones["end_date"], errors="coerce")

# Default all to NORMAL
buoy["label"] = "NORMAL"

# Update label to CYCLONE if within cyclone period
for _, row in cyclones.iterrows():
    start, end = row["start_date"], row["end_date"]
    if pd.notnull(start) and pd.notnull(end):
        mask = (buoy["date"] >= start) & (buoy["date"] <= end)
        buoy.loc[mask, "label"] = "CYCLONE"

# Save final dataset
buoy.to_csv("buoy_labeled.csv", index=False)

print(f"✅ Final dataset saved as buoy_labeled.csv with {len(buoy)} rows")
print(buoy["label"].value_counts())
