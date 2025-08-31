# backend/app/services/storm_surge_predictor.py
import requests
import logging
import os
import math
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

class StormSurgePredictor:
    def __init__(self):
        self.coastal_bathymetry = self.load_coastal_data()
        
    def load_coastal_data(self):
        """
        Load coastal bathymetry data for surge calculation
        In a real implementation, this would be detailed coastal depth data
        For hackathon purposes, we'll use simplified values
        """
        # Simplified coastal data - would be replaced with real data in production
        return {
            "mumbai": {
                "coastal_slope": 0.01,  # Gentle slope
                "typical_depth": 10.0,   # Meters
                "vulnerability_factor": 0.8  # High vulnerability
            },
            "default": {
                "coastal_slope": 0.02,
                "typical_depth": 15.0,
                "vulnerability_factor": 0.5
            }
        }
    
    def predict_storm_surge(self, weather_data: Dict[str, Any], location: str = "mumbai") -> Dict[str, Any]:
        """
        Predict storm surge height using meteorological data
        Based on the simplified formula: Surge = f(pressure, wind, coastal_geometry)
        """
        try:
            # Get current tidal data
            tidal_data = self.get_tidal_data(
                weather_data.get('lat', 19.0760),
                weather_data.get('lon', 72.8777)
            )
            
            # Calculate storm surge components
            pressure_surge = self.calculate_pressure_component(weather_data['pressure'])
            wind_surge = self.calculate_wind_component(
                weather_data['wind_speed'], 
                weather_data.get('wind_direction', 180)  # Default SW direction
            )
            
            # Get coastal factors
            coastal_factors = self.coastal_bathymetry.get(location, self.coastal_bathymetry["default"])
            
            # Combine components with coastal factors
            total_surge = (pressure_surge + wind_surge) * coastal_factors["vulnerability_factor"]
            
            # Add to tidal height for total water level
            total_water_level = tidal_data.get('current_height', 0) + total_surge
            
            return {
                "pressure_surge": round(pressure_surge, 2),
                "wind_surge": round(wind_surge, 2),
                "total_surge": round(total_surge, 2),
                "tidal_height": round(tidal_data.get('current_height', 0), 2),
                "total_water_level": round(total_water_level, 2),
                "prediction_time": datetime.now().isoformat(),
                "location": location,
                "threat_level": self.assess_threat_level(total_water_level, coastal_factors)
            }
            
        except Exception as e:
            logger.error(f"Error predicting storm surge: {e}")
            return {"error": str(e)}
    
    def calculate_pressure_component(self, pressure_hpa: float) -> float:
        """
        Calculate surge component from pressure difference
        Using the inverted barometer effect: ~1cm surge per 1hPa pressure drop
        """
        normal_pressure = 1013.25  # Standard atmospheric pressure
        pressure_drop = normal_pressure - pressure_hpa
        return max(0, pressure_drop * 0.01)  # Convert to meters
    
    def calculate_wind_component(self, wind_speed_kmh: float, wind_direction_deg: float) -> float:
        """
        Calculate surge component from wind stress
        Simplified formula based on wind speed and direction
        """
        # Convert wind speed to m/s (more standard for calculations)
        wind_speed_ms = wind_speed_kmh / 3.6
        
        # Factor based on wind direction (onshore winds cause more surge)
        # Assuming 180° is directly onshore (simplified)
        direction_factor = max(0, math.cos(math.radians(wind_direction_deg - 180)))
        
        # Wind stress formula (simplified)
        return (wind_speed_ms ** 2) * direction_factor * 0.0005
    
    def get_tidal_data(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """
        Fetch tidal data from WorldTides API
        """
        try:
            api_key = os.getenv("WORLDTIDE_API_KEY")
            if not api_key:
                logger.warning("WorldTides API key not configured")
                return {"current_height": 0}
            
            # Get current time for tidal prediction
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            response = requests.get(
                "https://www.worldtides.info/api/v2",
                params={
                    "key": api_key,
                    "lat": latitude,
                    "lon": longitude,
                    "date": current_time,
                    "length": 1,  # 1 day of data
                    "step": 60,   # 60-minute intervals
                    "datum": "CD"  # Chart Datum
                },
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                # Extract current tidal height
                # The API returns heights array with timestamps and heights
                if 'heights' in data and len(data['heights']) > 0:
                    # Find the closest time to current
                    current_epoch = datetime.now().timestamp()
                    closest_tide = min(data['heights'], key=lambda x: abs(x['dt'] - current_epoch))
                    return {"current_height": closest_tide['height']}
                else:
                    logger.warning("No tidal data found in API response")
                    return {"current_height": 0}
            else:
                logger.error(f"WorldTides API returned status code: {response.status_code}")
                return {"current_height": 0}
                
        except Exception as e:
            logger.error(f"Error fetching tidal data: {e}")
            return {"current_height": 0}
    
    def assess_threat_level(self, water_level: float, coastal_factors: Dict[str, float]) -> str:
        """
        Assess threat level based on water level and coastal vulnerability
        """
        # These thresholds would be calibrated for each location
        base_threshold = 2.0  # meters above chart datum
        
        # Adjust threshold based on coastal vulnerability
        adjusted_threshold = base_threshold * (1 / coastal_factors["vulnerability_factor"])
        
        if water_level > adjusted_threshold + 1.0:
            return "extreme"
        elif water_level > adjusted_threshold:
            return "high"
        elif water_level > adjusted_threshold - 0.5:
            return "moderate"
        else:
            return "low"

# Create a singleton instance
storm_surge_predictor = StormSurgePredictor()