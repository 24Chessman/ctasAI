#!/usr/bin/env python3
"""
Test datetime serialization fix
"""

import json
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

def test_datetime_serialization():
    """Test if datetime serialization is working"""
    
    print("🧪 Testing DateTime Serialization...")
    
    try:
        from app.core.utils import serialize_datetime, clean_profile_data
        from datetime import datetime
        
        # Test data with datetime objects
        test_data = {
            "id": "123",
            "email": "test@example.com",
            "full_name": "Test User",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        print("   Original data:")
        print(f"   {test_data}")
        
        # Test serialize_datetime function
        serialized = serialize_datetime(test_data)
        print("\n   After serialize_datetime:")
        print(f"   {serialized}")
        
        # Test JSON serialization
        json_str = json.dumps(serialized)
        print("\n   JSON serialization successful:")
        print(f"   {json_str}")
        
        # Test clean_profile_data function
        cleaned = clean_profile_data(test_data)
        print("\n   After clean_profile_data:")
        print(f"   {cleaned}")
        
        # Test JSON serialization of cleaned data
        cleaned_json = json.dumps(cleaned)
        print("\n   Cleaned data JSON serialization successful:")
        print(f"   {cleaned_json}")
        
        print("\n✅ DateTime serialization is working correctly!")
        return True
        
    except Exception as e:
        print(f"\n❌ DateTime serialization test failed: {e}")
        return False

def test_auth_service_datetime():
    """Test auth service datetime handling"""
    
    print("\n🔐 Testing Auth Service DateTime Handling...")
    
    try:
        from app.services.auth_service import auth_service
        
        # Test login with a non-existent user (should return error but not datetime error)
        result = auth_service.login_user("nonexistent@example.com", "wrongpassword")
        
        print(f"   Auth service result: {result}")
        
        # Check if result is JSON serializable
        json.dumps(result)
        print("   ✅ Auth service result is JSON serializable")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Auth service test failed: {e}")
        return False

def main():
    """Main test function"""
    
    print("🚀 DateTime Serialization Test")
    print("=" * 50)
    
    # Test datetime serialization
    datetime_ok = test_datetime_serialization()
    
    # Test auth service
    auth_ok = test_auth_service_datetime()
    
    print("\n" + "=" * 50)
    
    if datetime_ok and auth_ok:
        print("🎉 All datetime serialization tests passed!")
        print("\nThe datetime serialization fix is working correctly.")
        print("If you're still seeing the error in the frontend,")
        print("the issue might be:")
        print("1. Backend server not running")
        print("2. Frontend not connecting to backend")
        print("3. CORS issues")
        print("4. Browser cache issues")
    else:
        print("❌ Some datetime serialization tests failed!")
        print("Please check the error messages above.")

if __name__ == "__main__":
    main()
