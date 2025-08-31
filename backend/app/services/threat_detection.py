# backend/app/services/threat_detection.py
import logging
from datetime import datetime
from app.services.data_fetcher import fetch_weather_data
from app.ml_models.cyclone_predictor import cyclone_predictor
from app.services.storm_surge_predictor import storm_surge_predictor

logger = logging.getLogger(__name__)

def run_threat_detection():
    """
    Run complete threat detection and return results
    """
    try:
        # Fetch current weather data
        weather_data = fetch_weather_data()
        logger.info(f"Fetched weather data: {weather_data}")
        
        # 1. Cyclone Prediction
        cyclone_data = cyclone_predictor.predict(weather_data)
        logger.info(f"Cyclone prediction: {cyclone_data}")
        
        # 2. Storm Surge Prediction
        surge_data = storm_surge_predictor.predict_storm_surge(weather_data)
        logger.info(f"Storm surge prediction: {surge_data}")
        
        # Determine overall threat level
        threat_level = determine_overall_threat(cyclone_data, surge_data)
        
        # Prepare response
        threat_data = {
            "timestamp": datetime.now().isoformat(),
            "weather_data": weather_data,
            "cyclone": cyclone_data,
            "storm_surge": surge_data,
            "overall_threat": threat_level,
            "recommendations": generate_recommendations(threat_level)
        }
        
        logger.info(f"Threat detection completed: {threat_data}")
        return threat_data
        
    except Exception as e:
        logger.error(f"Error in threat detection: {e}")
        # Return a safe default response in case of error
        return {
            "timestamp": datetime.now().isoformat(),
            "error": "System temporarily unavailable",
            "overall_threat": "UNKNOWN",
            "recommendations": ["System temporarily unavailable. Please try again later."]
        }

def determine_overall_threat(cyclone_data, surge_data):
    """
    Determine the overall threat level based on cyclone and surge data
    """
    # Check cyclone threat
    cyclone_threat = False
    if (cyclone_data.get("classification") == "CYCLONE" and 
        cyclone_data.get("probability", 0) > 0.7):
        cyclone_threat = True
    
    # Check storm surge threat
    surge_threat = surge_data.get("threat_level", "low") in ["high", "extreme"]
    
    # Determine overall threat
    if cyclone_threat or surge_threat:
        return "HIGH"
    elif surge_data.get("threat_level") == "medium":
        return "MEDIUM"
    else:
        return "LOW"

def generate_recommendations(threat_level):
    """
    Generate recommendations based on threat level
    """
    if threat_level == "HIGH":
        return [
            "Evacuate immediately if instructed by authorities",
            "Move to higher ground away from coastal areas",
            "Follow emergency services instructions"
        ]
    elif threat_level == "MEDIUM":
        return [
            "Prepare evacuation plan",
            "Secure property against potential flooding",
            "Monitor weather updates regularly"
        ]
    else:
        return [
            "Continue normal activities",
            "Stay informed about weather conditions",
            "Review emergency preparedness plans"
        ]