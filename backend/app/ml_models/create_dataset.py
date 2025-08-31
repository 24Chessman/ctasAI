import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate date range for the past 365 days
start_date = datetime.now() - timedelta(days=365)
dates = [start_date + timedelta(days=i) for i in range(365)]

# Initialize data with normal values
data = []
for date in dates:
    # Normal ranges
    wind_speed = np.random.uniform(5, 30)
    pressure = np.random.uniform(1010, 1020)
    wave_height = np.random.uniform(0.5, 2.0)
    water_level = np.random.uniform(0.0, 1.0)  # relative to normal tide
    label = 'NORMAL'
    data.append([date, wind_speed, pressure, wave_height, water_level, label])

# Create DataFrame
df = pd.DataFrame(data, columns=['date', 'wind_speed', 'pressure', 'wave_height', 'water_level', 'label'])

# Convert date to datetime if not already
df['date'] = pd.to_datetime(df['date'])

# Now, override for known cyclone events
cyclone_dates = ['2023-05-15', '2023-11-10']
for cd in cyclone_dates:
    cyclone_date = pd.to_datetime(cd)
    idx = df[df['date'] == cyclone_date].index
    if len(idx) > 0:
        idx = idx[0]
        df.at[idx, 'wind_speed'] = np.random.uniform(60, 100)
        df.at[idx, 'pressure'] = np.random.uniform(970, 1000)
        df.at[idx, 'wave_height'] = np.random.uniform(3, 10)
        df.at[idx, 'water_level'] = np.random.uniform(2, 5)
        df.at[idx, 'label'] = 'CYCLONE'

# Similarly for flood events
flood_dates = ['2023-07-20', '2023-08-15']
for fd in flood_dates:
    flood_date = pd.to_datetime(fd)
    idx = df[df['date'] == flood_date].index
    if len(idx) > 0:
        idx = idx[0]
        df.at[idx, 'wind_speed'] = np.random.uniform(20, 40)
        df.at[idx, 'pressure'] = np.random.uniform(1000, 1010)
        df.at[idx, 'wave_height'] = np.random.uniform(1.5, 3.0)
        df.at[idx, 'water_level'] = np.random.uniform(2, 4)
        df.at[idx, 'label'] = 'FLOOD'

# Save to CSV
df.to_csv('historical_data_labeled.csv', index=False)