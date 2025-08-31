# backend/app/api/endpoints/evacuation.py
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Optional
from datetime import datetime
from app.services.notification_service import notification_service
from app.services.threat_detection import run_threat_detection

router = APIRouter()

@router.post("/trigger-evacuation")
async def trigger_evacuation_alert(
    location: Optional[str] = None,
    threat_level: Optional[str] = "HIGH",
    custom_message: Optional[str] = None
):
    """
    Manually trigger evacuation alert for testing purposes
    """
    try:
        # Create mock threat data for testing
        mock_threat_data = {
            "timestamp": datetime.now().isoformat(),
            "overall_threat": threat_level,
            "cyclone": {
                "classification": "CYCLONE",
                "probability": 0.85,
                "intensity": "Category 3"
            },
            "storm_surge": {
                "threat_level": "high",
                "total_water_level": 3.5,
                "surge_height": 2.1
            },
            "weather_data": {
                "wind_speed": 45,
                "pressure": 980,
                "temperature": 25
            },
            "recommendations": [
                "Evacuate immediately if instructed by authorities",
                "Move to higher ground away from coastal areas",
                "Follow emergency services instructions"
            ]
        }
        
        # Get users by location if specified
        target_users = None
        if location:
            target_users = notification_service.get_users_by_location(location)
            if not target_users:
                return {
                    "success": False,
                    "message": f"No users found in location: {location}",
                    "sent_count": 0
                }
        
        # Send evacuation alert
        result = notification_service.send_evacuation_alert(mock_threat_data, target_users)
        
        return {
            "success": result["success"],
            "message": result["message"],
            "threat_data": mock_threat_data,
            "results": result.get("results", {}),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error triggering evacuation alert: {str(e)}")

@router.post("/test-evacuation")
async def test_evacuation_system():
    """
    Test the evacuation system with real threat detection
    """
    try:
        # Run actual threat detection
        threat_data = run_threat_detection()
        
        # Check if threat level is high enough to trigger evacuation
        if threat_data.get("overall_threat") in ["HIGH", "high", "extreme"]:
            # Send evacuation alert
            result = notification_service.send_evacuation_alert(threat_data)
            
            return {
                "success": result["success"],
                "message": result["message"],
                "threat_data": threat_data,
                "results": result.get("results", {}),
                "timestamp": datetime.now().isoformat(),
                "note": "Real threat detected and evacuation alert sent"
            }
        else:
            return {
                "success": True,
                "message": "No evacuation needed - threat level is low",
                "threat_data": threat_data,
                "threat_level": threat_data.get("overall_threat"),
                "timestamp": datetime.now().isoformat(),
                "note": "Current threat level does not require evacuation"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error testing evacuation system: {str(e)}")

@router.get("/users")
async def get_registered_users():
    """
    Get list of registered users (for admin purposes)
    """
    try:
        users = notification_service.get_all_users()
        
        # Return user count and basic info (without sensitive data)
        user_info = []
        for user in users:
            user_info.append({
                "id": user.get("id"),
                "full_name": user.get("full_name"),
                "email": user.get("email")[:3] + "***" if user.get("email") else None,
                "has_phone": bool(user.get("phone")),
                "has_device_token": bool(user.get("device_token")),
                "location": user.get("location", "Unknown")
            })
        
        return {
            "total_users": len(users),
            "users": user_info,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")

@router.get("/users/location/{location}")
async def get_users_by_location(location: str):
    """
    Get users by specific location
    """
    try:
        users = notification_service.get_users_by_location(location)
        
        user_info = []
        for user in users:
            user_info.append({
                "id": user.get("id"),
                "full_name": user.get("full_name"),
                "email": user.get("email")[:3] + "***" if user.get("email") else None,
                "has_phone": bool(user.get("phone")),
                "has_device_token": bool(user.get("device_token")),
                "location": user.get("location", "Unknown")
            })
        
        return {
            "location": location,
            "total_users": len(users),
            "users": user_info,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users by location: {str(e)}")

@router.post("/send-custom-alert")
async def send_custom_alert(
    message: str,
    title: str = "Custom Alert",
    target_location: Optional[str] = None
):
    """
    Send a custom alert message to users
    """
    try:
        # Create custom threat data
        custom_threat_data = {
            "timestamp": datetime.now().isoformat(),
            "overall_threat": "CUSTOM",
            "custom_message": message,
            "custom_title": title,
            "recommendations": [message]
        }
        
        # Get target users
        target_users = None
        if target_location:
            target_users = notification_service.get_users_by_location(target_location)
        
        # Send custom alert
        result = notification_service.send_evacuation_alert(custom_threat_data, target_users)
        
        return {
            "success": result["success"],
            "message": result["message"],
            "custom_data": {
                "title": title,
                "message": message,
                "target_location": target_location
            },
            "results": result.get("results", {}),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending custom alert: {str(e)}")
