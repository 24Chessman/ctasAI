# app/api/endpoints/alerts.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from app.services.notification_service import notification_service
from app.services.alert_system import check_and_send_alerts
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class TestNotificationRequest(BaseModel):
    threat_level: str = "HIGH"
    cyclone_probability: float = 0.8
    storm_surge_level: str = "high"
    water_level: float = 3.0
    test_email: str = None

@router.get("/")
async def get_alerts():
    return {"message": "Alerts endpoint is working"}

@router.post("/test-notification")
async def test_notification(request: TestNotificationRequest):
    """
    Test endpoint to manually trigger notifications
    """
    try:
        # Create test threat data
        test_threat_data = {
            "overall_threat": request.threat_level,
            "cyclone": {
                "classification": "CYCLONE" if request.cyclone_probability > 0.5 else "NO_CYCLONE",
                "probability": request.cyclone_probability,
                "wind_speed": 120 if request.threat_level == "HIGH" else 25,
                "pressure": 950 if request.threat_level == "HIGH" else 1013
            },
            "storm_surge": {
                "threat_level": request.storm_surge_level,
                "total_water_level": request.water_level,
                "surge_height": request.water_level * 0.8,
                "tide_height": request.water_level * 0.2
            },
            "timestamp": "2024-01-15T14:30:00Z"
        }
        
        # If test email provided, create a temporary user list
        target_users = None
        if request.test_email:
            target_users = [{"email": request.test_email, "id": "test_user"}]
        
        # Send evacuation alert
        result = notification_service.send_evacuation_alert(test_threat_data, target_users)
        
        return {
            "success": True,
            "message": "Test notification triggered",
            "threat_data": test_threat_data,
            "notification_result": result
        }
        
    except Exception as e:
        logger.error(f"Error testing notification: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-alert-system")
async def test_alert_system():
    """
    Test endpoint to trigger the full alert system
    """
    try:
        # Test data that should trigger alerts
        test_prediction = {
            "overall_threat": "HIGH",
            "cyclone": {
                "classification": "CYCLONE",
                "probability": 0.8,
                "wind_speed": 110,
                "pressure": 960
            },
            "storm_surge": {
                "threat_level": "high",
                "total_water_level": 2.8,
                "surge_height": 2.1,
                "tide_height": 0.7
            }
        }
        
        test_weather_data = {
            "wind_speed": 110,
            "pressure": 960,
            "temperature": 25,
            "humidity": 85
        }
        
        # Trigger alert system
        check_and_send_alerts(test_prediction, test_weather_data)
        
        return {
            "success": True,
            "message": "Alert system test triggered",
            "test_data": {
                "prediction": test_prediction,
                "weather": test_weather_data
            }
        }
        
    except Exception as e:
        logger.error(f"Error testing alert system: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users")
async def get_users():
    """
    Get all users for testing purposes
    """
    try:
        users = notification_service.get_all_users()
        return {
            "success": True,
            "user_count": len(users),
            "users": users[:10]  # Return first 10 users for privacy
        }
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# You can add more alert-related endpoints here later