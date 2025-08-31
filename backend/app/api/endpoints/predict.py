# backend/app/api/endpoints/predict.py
from fastapi import APIRouter, HTTPException
from app.services.prediction_service import prediction_service
from app.services.threat_detection import run_threat_detection
import pandas as pd
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/predict")
async def predict_cyclone(data: dict):
    """
    Predict cyclone probability from sensor data
    
    Expected data format:
    {
        "wind_speed": 15.2,
        "pressure": 1005.3,
        "wave_height": 3.2,
        "water_level": 1.5,
        "hour": 14,
        "day_of_year": 243,
        "month": 8,
        "day_of_week": 2,
        "is_weekend": 0,
        "pressure_change_6h": -2.1,
        "wind_speed_change_6h": 5.3,
        "pressure_trend": 1007.1,
        "wind_speed_trend": 12.8,
        "pressure_std_12h": 1.2,
        "wave_height_change": 0.8,
        "pressure_drop_rate": -0.35
    }
    """
    try:
        result = prediction_service.predict_cyclone(data)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        # Format response to match frontend expectations
        return {
            "status": "success",
            "data": result,
            "message": "Prediction completed successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/threat-detection")
async def threat_detection():
    """
    Run comprehensive threat detection (cyclone + storm surge)
    and return the results
    """
    try:
        # Run the threat detection
        threat_data = run_threat_detection() 
        
        return {
            "status": "success",
            "data": threat_data,
            "message": "Threat assessment completed successfully"
        }
    except Exception as e:
        logger.error(f"Error in threat detection: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Failed to complete threat assessment"
        )

@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify the prediction service is working
    """
    return {
        "status": "healthy", 
        "message": "Cyclone prediction service is running"
    }