"""
Utility functions for CTAS AI Backend
"""
import json
from datetime import datetime, date
from typing import Any, Dict, List, Union

def serialize_datetime(obj: Any) -> Any:
    """
    Recursively serialize datetime objects to ISO format strings
    
    Args:
        obj: Object to serialize
        
    Returns:
        Serialized object with datetime objects converted to strings
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, date):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {key: serialize_datetime(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [serialize_datetime(item) for item in obj]
    else:
        return obj

def clean_profile_data(profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean profile data by removing sensitive fields and serializing datetimes
    
    Args:
        profile: Raw profile data from database
        
    Returns:
        Cleaned profile data safe for API responses
    """
    if not profile:
        return {}
    
    # Fields to include in API responses
    safe_fields = {
        'id', 'email', 'full_name', 'phone', 'location', 'role', 
        'created_at', 'updated_at'
    }
    
    # Filter and clean the profile data
    cleaned_profile = {}
    for key, value in profile.items():
        if key in safe_fields and value is not None:
            cleaned_profile[key] = value
    
    # Serialize datetime objects
    return serialize_datetime(cleaned_profile)

def safe_json_response(data: Any) -> Dict[str, Any]:
    """
    Prepare data for safe JSON response by serializing datetime objects
    
    Args:
        data: Data to prepare for JSON response
        
    Returns:
        Data safe for JSON serialization
    """
    return serialize_datetime(data)

def format_datetime(dt: Union[datetime, str, None]) -> str:
    """
    Format datetime object to readable string
    
    Args:
        dt: Datetime object or string
        
    Returns:
        Formatted datetime string
    """
    if dt is None:
        return ""
    
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
        except ValueError:
            return dt
    
    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    
    return str(dt)
