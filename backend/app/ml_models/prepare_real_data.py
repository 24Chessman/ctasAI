# app/ml_models/prepare_real_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import time
from typing import List, Dict, Optional

class HistoricalDataPreparer:
    def __init__(self):
        self.cyclone_events = []
        self.flood_events = []
        self.normal_periods = []
        
    def load_historical_events(self):
        """
        Load historical cyclone and flood events for the Indian coast.
        You'll need to research and add actual historical events here.
        """
        # Example data - REPLACE WITH ACTUAL HISTORICAL EVENTS
        self.cyclone_events = [
            {'name': 'Cyclone Biparjoy', 'start_date': '2023-06-06', 'end_date': '2023-06-16', 'peak_date': '2023-06-15'},
            {'name': 'Cyclone Tauktae', 'start_date': '2021-05-14', 'end_date': '2021-05-19', 'peak_date': '2021-05-17'},
            # Add more cyclones from IMD records
        ]
        
        self.flood_events = [
            {'name': 'Mumbai Floods', 'date': '2023-07-18', 'severity': 'high'},
            {'name': 'Chennai Floods', 'date': '2022-11-10', 'severity': 'medium'},
            # Add more flood events
        ]
        
        # Normal periods (no events)
        self.normal_periods = [
            {'start_date': '2023-04-01', 'end_date': '2023-04-15'},
            {'start_date': '2023-08-01', 'end_date': '2023-08-15'},
            # Add more normal periods
        ]
    
    def fetch_weather_data(self, date: str, location: str = "Mumbai") -> Optional[Dict]:
        """
        Fetch historical weather data for a specific date.
        Note: OpenWeatherMap historical data requires a paid plan.
        You might need to use alternative sources or manual data entry.
        """
        try:
            # This is a placeholder - you'll need a paid API for historical data
            # Alternatively, use data from IMD or other free sources
            api_key = "e77778f551addbbba0d6880b39ae0674"  # Replace with your actual key
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&dt={int(datetime.strptime(date, '%Y-%m-%d').timestamp())}&appid={api_key}"
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    'wind_speed': data.get('wind', {}).get('speed', 0),
                    'pressure': data.get('main', {}).get('pressure', 1013),
                    'humidity': data.get('main', {}).get('humidity', 0),
                    'temp': data.get('main', {}).get('temp', 0)
                }
        except Exception as e:
            print(f"Error fetching weather data for {date}: {e}")
        
        return None
    
    def generate_synthetic_tidal_data(self, date: str, event_type: str = "NORMAL") -> Dict:
        """
        Generate realistic tidal data based on event type.
        Replace this with actual INCOIS API data if available.
        """
        # Base values for normal conditions
        base_wave_height = np.random.uniform(0.5, 2.0)
        base_water_level = np.random.uniform(0.0, 1.0)
        
        if event_type == "CYCLONE":
            # Enhanced values for cyclones
            wave_height = base_wave_height * np.random.uniform(2.0, 4.0)
            water_level = base_water_level * np.random.uniform(1.5, 3.0)
        elif event_type == "FLOOD":
            # Enhanced values for floods
            wave_height = base_wave_height * np.random.uniform(1.5, 2.5)
            water_level = base_water_level * np.random.uniform(2.0, 4.0)
        else:
            # Normal conditions
            wave_height = base_wave_height
            water_level = base_water_level
        
        return {
            'wave_height': round(wave_height, 2),
            'water_level': round(water_level, 2)
        }
    
    def create_dataset(self):
        """
        Create the historical dataset with labeled events.
        """
        self.load_historical_events()
        dataset = []
        
        # Add cyclone events
        for event in self.cyclone_events:
            start_date = datetime.strptime(event['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(event['end_date'], '%Y-%m-%d')
            peak_date = datetime.strptime(event['peak_date'], '%Y-%m-%d')
            
            current_date = start_date
            while current_date <= end_date:
                date_str = current_date.strftime('%Y-%m-%d')
                
                # Fetch or generate weather data
                weather_data = self.fetch_weather_data(date_str)
                if not weather_data:
                    # Fallback to synthetic data if API fails
                    weather_data = {
                        'wind_speed': np.random.uniform(40, 100) if current_date >= peak_date else np.random.uniform(20, 50),
                        'pressure': np.random.uniform(970, 1000) if current_date >= peak_date else np.random.uniform(1000, 1015),
                        'humidity': np.random.uniform(70, 95),
                        'temp': np.random.uniform(25, 35)
                    }
                
                # Generate tidal data
                tidal_data = self.generate_synthetic_tidal_data(date_str, "CYCLONE")
                
                # Determine label intensity
                days_from_peak = abs((current_date - peak_date).days)
                if days_from_peak <= 1:
                    label = "CYCLONE"
                elif days_from_peak <= 3:
                    label = "STORM"  # Developing storm
                else:
                    label = "NORMAL"
                
                dataset.append({
                    'date': date_str,
                    'wind_speed': round(weather_data['wind_speed'], 2),
                    'pressure': round(weather_data['pressure'], 2),
                    'wave_height': tidal_data['wave_height'],
                    'water_level': tidal_data['water_level'],
                    'label': label
                })
                
                current_date += timedelta(days=1)
                time.sleep(0.1)  # Rate limiting
        
        # Add flood events (simplified)
        for event in self.flood_events:
            date_str = event['date']
            weather_data = self.fetch_weather_data(date_str) or {
                'wind_speed': np.random.uniform(20, 40),
                'pressure': np.random.uniform(1005, 1015),
                'humidity': np.random.uniform(80, 95),
                'temp': np.random.uniform(25, 32)
            }
            
            tidal_data = self.generate_synthetic_tidal_data(date_str, "FLOOD")
            
            dataset.append({
                'date': date_str,
                'wind_speed': round(weather_data['wind_speed'], 2),
                'pressure': round(weather_data['pressure'], 2),
                'wave_height': tidal_data['wave_height'],
                'water_level': tidal_data['water_level'],
                'label': "FLOOD"
            })
        
        # Add normal periods
        for period in self.normal_periods:
            start_date = datetime.strptime(period['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(period['end_date'], '%Y-%m-%d')
            
            current_date = start_date
            while current_date <= end_date:
                date_str = current_date.strftime('%Y-%m-%d')
                weather_data = self.fetch_weather_data(date_str) or {
                    'wind_speed': np.random.uniform(5, 20),
                    'pressure': np.random.uniform(1010, 1020),
                    'humidity': np.random.uniform(50, 80),
                    'temp': np.random.uniform(28, 35)
                }
                
                tidal_data = self.generate_synthetic_tidal_data(date_str, "NORMAL")
                
                dataset.append({
                    'date': date_str,
                    'wind_speed': round(weather_data['wind_speed'], 2),
                    'pressure': round(weather_data['pressure'], 2),
                    'wave_height': tidal_data['wave_height'],
                    'water_level': tidal_data['water_level'],
                    'label': "NORMAL"
                })
                
                current_date += timedelta(days=1)
                time.sleep(0.1)
        
        return dataset
    
    def save_dataset(self, dataset, filename="historical_real_data.csv"):
        """Save the dataset to a CSV file."""
        df = pd.DataFrame(dataset)
        df.to_csv(filename, index=False)
        print(f"Dataset saved to {filename} with {len(df)} records")
        return df

def main():
    """Main function to prepare the historical dataset."""
    print("Starting historical data preparation...")
    
    preparer = HistoricalDataPreparer()
    dataset = preparer.create_dataset()
    
    if dataset:
        df = preparer.save_dataset(dataset)
        print("\nDataset summary:")
        print(f"Total records: {len(df)}")
        print("\nLabel distribution:")
        print(df['label'].value_counts())
        
        # Show sample data
        print("\nSample data:")
        print(df.head(10))
    else:
        print("Failed to create dataset.")

if __name__ == "__main__":
    main()