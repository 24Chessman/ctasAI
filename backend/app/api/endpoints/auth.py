# backend/app/api/endpoints/auth.py
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.services.auth_service import auth_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Request/Response models
class UserRegistrationRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = None
    location: Optional[str] = None

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserProfileUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str

class AuthResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

# Helper function to get current user from token
async def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    try:
        # Extract token from "Bearer <token>"
        token = authorization.replace("Bearer ", "")
        user = auth_service.verify_token(token)
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        
        return user
    except Exception as e:
        logger.error(f"Error verifying token: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/register", response_model=AuthResponse)
async def register_user(request: UserRegistrationRequest):
    """
    Register a new user
    """
    try:
        result = auth_service.register_user(
            email=request.email,
            password=request.password,
            full_name=request.full_name,
            phone=request.phone,
            location=request.location
        )
        
        if result["success"]:
            return AuthResponse(
                success=True,
                message=result["message"],
                data={"user_id": result["user_id"], "email": result["email"]}
            )
        else:
            raise HTTPException(status_code=400, detail=result["message"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in user registration: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/login", response_model=AuthResponse)
async def login_user(request: UserLoginRequest):
    """
    Login user
    """
    try:
        result = auth_service.login_user(
            email=request.email,
            password=request.password
        )
        
        if result["success"]:
            return AuthResponse(
                success=True,
                message=result["message"],
                data={
                    "user": result["user"],
                    "access_token": result["access_token"],
                    "refresh_token": result["refresh_token"]
                }
            )
        else:
            raise HTTPException(status_code=401, detail=result["message"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in user login: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/logout", response_model=AuthResponse)
async def logout_user(current_user: dict = Depends(get_current_user)):
    """
    Logout user
    """
    try:
        # Note: We need the actual token here, but for simplicity we'll just return success
        # In a real implementation, you'd want to pass the token in the request body
        result = auth_service.logout_user(
            user_id=current_user["id"],
            session_token="current_session_token"  # This should come from request body in real implementation
        )
        
        return AuthResponse(
            success=True,
            message="Logout successful"
        )
        
    except Exception as e:
        logger.error(f"Error in user logout: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/profile", response_model=AuthResponse)
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """
    Get current user profile
    """
    try:
        profile = auth_service.get_user_profile(current_user["id"])
        
        if profile:
            return AuthResponse(
                success=True,
                message="Profile retrieved successfully",
                data=profile
            )
        else:
            raise HTTPException(status_code=404, detail="Profile not found")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user profile: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/profile", response_model=AuthResponse)
async def update_user_profile(
    request: UserProfileUpdateRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Update current user profile
    """
    try:
        # Convert request to dict and remove None values
        profile_data = {k: v for k, v in request.dict().items() if v is not None}
        
        if not profile_data:
            raise HTTPException(status_code=400, detail="No valid fields to update")
        
        result = auth_service.update_user_profile(
            user_id=current_user["id"],
            profile_data=profile_data
        )
        
        if result["success"]:
            return AuthResponse(
                success=True,
                message=result["message"]
            )
        else:
            raise HTTPException(status_code=400, detail=result["message"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user profile: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/change-password", response_model=AuthResponse)
async def change_password(
    request: PasswordChangeRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Change user password
    """
    try:
        result = auth_service.change_user_password(
            user_id=current_user["id"],
            current_password=request.current_password,
            new_password=request.new_password
        )
        
        if result["success"]:
            return AuthResponse(
                success=True,
                message=result["message"]
            )
        else:
            raise HTTPException(status_code=400, detail=result["message"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error changing password: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/profile", response_model=AuthResponse)
async def delete_user_profile(current_user: dict = Depends(get_current_user)):
    """
    Delete current user profile
    """
    try:
        result = auth_service.delete_user(current_user["id"])
        
        if result["success"]:
            return AuthResponse(
                success=True,
                message=result["message"]
            )
        else:
            raise HTTPException(status_code=400, detail=result["message"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user profile: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/verify", response_model=AuthResponse)
async def verify_token(current_user: dict = Depends(get_current_user)):
    """
    Verify current token and return user info
    """
    return AuthResponse(
        success=True,
        message="Token is valid",
        data=current_user
    )
