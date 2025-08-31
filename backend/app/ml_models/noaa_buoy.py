# synthetic_buoy.py
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Config
START_DATE = datetime(2015, 1, 1)
END_DATE = datetime(2023, 12, 31)
OUTPUT_FILE = "buoy.csv"

# Generate date range (hourly data)
date_range = pd.date_range(start=START_DATE, end=END_DATE, freq="6H")

data = []

for d in date_range:
    # Randomly decide if cyclone occurs (1% chance)
    is_cyclone = random.random() < 0.01
    
    if is_cyclone:
        wind_speed = np.random.uniform(15, 40)     # m/s
        pressure = np.random.uniform(950, 995)     # hPa
        wave_height = np.random.uniform(3, 12)     # m
        water_level = np.random.uniform(1.5, 4.0)  # m
        label = "CYCLONE"
    else:
        wind_speed = np.random.uniform(2, 8)       # m/s
        pressure = np.random.uniform(1005, 1015)   # hPa
        wave_height = np.random.uniform(0.5, 2.0)  # m
        water_level = np.random.uniform(0.2, 1.0)  # m
        label = "NORMAL"
    
    data.append([d.strftime("%Y-%m-%d %H:%M:%S"),
                 round(wind_speed, 2),
                 round(pressure, 2),
                 round(wave_height, 2),
                 round(water_level, 2),
                 label])

# Save to CSV
df = pd.DataFrame(data, columns=["date", "wind_speed", "pressure", "wave_height", "water_level", "label"])
df.to_csv(OUTPUT_FILE, index=False)

print(f"✅ Generated synthetic buoy dataset with {len(df)} rows -> {OUTPUT_FILE}")
print(df.head(10))
