# backend/app/services/data_fetcher.py
import requests
import logging
import os
import random
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

def get_api_config():
    """
    Dynamically get API configuration with current environment variables
    """
    return {
        "weatherapi": {
            "url": "http://api.weatherapi.com/v1/current.json",
            "params": {
                "key": os.getenv("WEATHERAPI_API_KEY", ""),
                "q": f"{os.getenv('DEFAULT_LATITUDE', '19.0760')},{os.getenv('DEFAULT_LONGITUDE', '72.8777')}",
                "aqi": "no"
            }
        },
        "openweathermap": {
            "url": "https://api.openweathermap.org/data/2.5/weather",
            "params": {
                "appid": os.getenv("OPENWEATHERMAP_API_KEY", ""),
                "lat": os.getenv("DEFAULT_LATITUDE", "19.0760"),
                "lon": os.getenv("DEFAULT_LONGITUDE", "72.8777"),
                "units": "metric"
            }
        }
    }

def fetch_weather_data(latitude: float = None, longitude: float = None):
    """
    Fetch real-time weather data from available APIs
    """
    try:
        # Use provided coordinates or defaults
        lat = latitude if latitude else float(os.getenv("DEFAULT_LATITUDE", "19.0760"))
        lon = longitude if longitude else float(os.getenv("DEFAULT_LONGITUDE", "72.8777"))
        
        # Try WeatherAPI first
        data = fetch_from_weatherapi(lat, lon)
        if data and data.get('valid', True):
            return data
            
        # Fallback to OpenWeatherMap if WeatherAPI fails
        data = fetch_from_openweathermap(lat, lon)
        if data and data.get('valid', True):
            return data
            
        # If all APIs fail, use simulation as fallback
        logger.warning("All real data APIs failed, using simulated data")
        return generate_simulated_data()
        
    except Exception as e:
        logger.error(f"Error fetching weather data: {e}")
        return generate_simulated_data()

def fetch_from_weatherapi(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Fetch data from WeatherAPI
    """
    try:
        api_key = os.getenv("WEATHERAPI_API_KEY")
        if not api_key:
            logger.warning("WeatherAPI key not configured")
            return {"valid": False}
            
        api_config = get_api_config()
        params = api_config["weatherapi"]["params"].copy()
        params["q"] = f"{latitude},{longitude}"
        
        response = requests.get(
            api_config["weatherapi"]["url"],
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            current = data.get("current", {})
            
            # Extract relevant data
            return {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "wind_speed": current.get("wind_kph", 0),  # km/h
                "pressure": current.get("pressure_mb", 0),  # hPa (mb)
                "wave_height": estimate_wave_height(current.get("wind_kph", 0)),  # Estimated
                "water_level": estimate_water_level(current.get("pressure_mb", 0)),  # Estimated
                "source": "weatherapi",
                "humidity": current.get("humidity", 0),
                "temp_c": current.get("temp_c", 0),
                "valid": True
            }
        else:
            logger.error(f"WeatherAPI returned status code: {response.status_code}")
            logger.error(f"WeatherAPI response: {response.text}")
            return {"valid": False}
            
    except Exception as e:
        logger.error(f"Error fetching from WeatherAPI: {e}")
        return {"valid": False}

def fetch_from_openweathermap(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Fetch data from OpenWeatherMap API
    """
    try:
        api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if not api_key:
            logger.warning("OpenWeatherMap API key not configured")
            return {"valid": False}
            
        api_config = get_api_config()
        params = api_config["openweathermap"]["params"].copy()
        params["lat"] = latitude
        params["lon"] = longitude
        
        response = requests.get(
            api_config["openweathermap"]["url"],
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract wind speed (convert m/s to km/h)
            wind_speed = data.get("wind", {}).get("speed", 0) * 3.6
            
            # Extract pressure (hPa)
            pressure = data.get("main", {}).get("pressure", 0)
            
            return {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "wind_speed": round(wind_speed, 1),  # Converted to km/h
                "pressure": pressure,
                "wave_height": estimate_wave_height(wind_speed),  # Estimated
                "water_level": estimate_water_level(pressure),  # Estimated
                "source": "openweathermap",
                "humidity": data.get("main", {}).get("humidity", 0),
                "temp_c": data.get("main", {}).get("temp", 0),
                "valid": True
            }
        else:
            logger.error(f"OpenWeatherMap returned status code: {response.status_code}")
            logger.error(f"OpenWeatherMap response: {response.text}")
            return {"valid": False}
            
    except Exception as e:
        logger.error(f"Error fetching from OpenWeatherMap: {e}")
        return {"valid": False}

def estimate_wave_height(wind_speed: float) -> float:
    """
    Estimate wave height based on wind speed
    Using a simplified formula: wave_height = 0.0248 * wind_speed^2
    This is a rough estimation and should be replaced with better models
    """
    if wind_speed <= 0:
        return 0.0
    # Cap the estimation to reasonable values
    return min(12.0, max(0.1, 0.0248 * wind_speed * wind_speed))

def estimate_water_level(pressure: float) -> float:
    """
    Estimate water level based on atmospheric pressure
    Using a simplified formula: water_level = (1013.25 - pressure) * 0.01
    This estimates storm surge based on pressure differences
    """
    if pressure <= 0:
        return 0.0
    # Normal pressure is around 1013.25 hPa
    # Lower pressure typically means higher water levels (storm surge)
    return max(0.0, (1013.25 - pressure) * 0.01)

def generate_simulated_data() -> Dict[str, Any]:
    """
    Generate simulated data as fallback, including wave height and water level
    """
    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "wind_speed": round(random.uniform(5, 120), 1),
        "pressure": round(random.uniform(980, 1040), 1),
        "wave_height": round(random.uniform(0.5, 8.0), 1),
        "water_level": round(random.uniform(0.2, 3.5), 1),
        "source": "simulation",
        "valid": True
    }