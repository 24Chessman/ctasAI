# # backend/app/api/endpoints/sms.py
# from fastapi import APIRouter, HTTPException, Depends
# from pydantic import BaseModel, Field
# from typing import Optional, Dict, List
# import logging
# from app.services.sms_service import sms_service
# from app.services.auth_service import auth_service

# logger = logging.getLogger(__name__)

# router = APIRouter()

# class SMSAlertRequest(BaseModel):
#     threat_level: str = Field(..., description="Threat level (HIGH, MEDIUM, LOW)")
#     threat_data: Dict = Field(..., description="Threat data dictionary")
#     location: Optional[str] = Field(None, description="Optional location filter")
#     message: Optional[str] = Field(None, description="Custom message (optional)")

# class BulkSMSRequest(BaseModel):
#     phone_numbers: List[str] = Field(..., description="List of phone numbers")
#     message: str = Field(..., description="SMS message content")

# class SMSResponse(BaseModel):
#     success: bool
#     message: str
#     total_users: int = 0
#     successful: int = 0
#     failed: int = 0
#     errors: List[str] = []

# @router.post("/send-high-alert", response_model=SMSResponse)
# async def send_high_alert_sms(request: SMSAlertRequest):
#     """
#     Send high alert SMS to all users with phone numbers
#     """
#     try:
#         logger.info(f"Sending high alert SMS - Threat Level: {request.threat_level}")
        
#         # Validate threat level
#         if request.threat_level.upper() not in ["HIGH", "MEDIUM", "LOW"]:
#             raise HTTPException(status_code=400, detail="Invalid threat level. Must be HIGH, MEDIUM, or LOW")
        
#         # Send SMS alerts
#         result = sms_service.send_high_alert_sms(
#             threat_level=request.threat_level.upper(),
#             threat_data=request.threat_data,
#             location=request.location
#         )
        
#         return SMSResponse(**result)
        
#     except Exception as e:
#         logger.error(f"Error sending high alert SMS: {e}")
#         raise HTTPException(status_code=500, detail=f"Error sending SMS alerts: {str(e)}")

# @router.post("/send-bulk-sms", response_model=SMSResponse)
# async def send_bulk_sms(request: BulkSMSRequest):
#     """
#     Send SMS to specific phone numbers
#     """
#     try:
#         logger.info(f"Sending bulk SMS to {len(request.phone_numbers)} numbers")
        
#         # Create user-like objects for bulk SMS
#         users = [{"phone": phone, "email": f"user_{i}@example.com"} for i, phone in enumerate(request.phone_numbers)]
        
#         # Send bulk SMS
#         result = sms_service.send_bulk_sms_alert(users, request.message)
        
#         return SMSResponse(
#             success=result["successful"] > 0,
#             message=f"SMS sent to {result['successful']} out of {result['total_users']} numbers",
#             total_users=result["total_users"],
#             successful=result["successful"],
#             failed=result["failed"],
#             errors=result.get("errors", [])
#         )
        
#     except Exception as e:
#         logger.error(f"Error sending bulk SMS: {e}")
#         raise HTTPException(status_code=500, detail=f"Error sending bulk SMS: {str(e)}")

# @router.get("/users-with-phones")
# async def get_users_with_phone_numbers(location: Optional[str] = None):
#     """
#     Get all users with valid phone numbers
#     """
#     try:
#         users = sms_service.get_users_with_phone_numbers(location)
        
#         return {
#             "success": True,
#             "total_users": len(users),
#             "users": users
#         }
        
#     except Exception as e:
#         logger.error(f"Error fetching users with phone numbers: {e}")
#         raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")

# @router.post("/test-sms")
# async def test_sms(phone: str, message: str = "Test SMS from CTAS Alert System"):
#     """
#     Send a test SMS to verify configuration
#     """
#     try:
#         logger.info(f"Sending test SMS to {phone}")
        
#         success, error_msg = sms_service.send_sms_alert(phone, message)
        
#         if success:
#             return {
#                 "success": True,
#                 "message": "Test SMS sent successfully",
#                 "phone": phone
#             }
#         else:
#             return {
#                 "success": False,
#                 "message": f"Failed to send test SMS: {error_msg}",
#                 "phone": phone
#             }
        
#     except Exception as e:
#         logger.error(f"Error sending test SMS: {e}")
#         raise HTTPException(status_code=500, detail=f"Error sending test SMS: {str(e)}")

# @router.get("/sms-status")
# async def get_sms_status():
#     """
#     Get SMS service status and configuration
#     """
#     try:
#         # Check if SMS is configured
#         is_configured = bool(sms_service.sms_api_key and sms_service.sms_api_url)
        
#         # Get user count with phone numbers
#         users_with_phones = sms_service.get_users_with_phone_numbers()
        
#         return {
#             "sms_configured": is_configured,
#             "sms_provider": sms_service.sms_provider,
#             "users_with_phones": len(users_with_phones),
#             "api_key_configured": bool(sms_service.sms_api_key),
#             "api_url_configured": bool(sms_service.sms_api_url)
#         }
        
#     except Exception as e:
#         logger.error(f"Error getting SMS status: {e}")
#         raise HTTPException(status_code=500, detail=f"Error getting SMS status: {str(e)}")
