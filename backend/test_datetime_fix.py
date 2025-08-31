#!/usr/bin/env python3
"""
Test script to verify datetime serialization fix
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

def test_datetime_serialization():
    """Test if datetime objects can be properly serialized"""
    
    print("🕒 Testing DateTime Serialization...")
    
    try:
        from app.core.utils import serialize_datetime, clean_profile_data
        print("✅ Utility functions imported successfully")
        
        # Test datetime serialization
        from datetime import datetime, timedelta
        
        # Create test data with datetime objects
        test_data = {
            "id": "test-123",
            "email": "test@example.com",
            "created_at": datetime.now(),
            "updated_at": datetime.now() + timedelta(hours=1),
            "nested": {
                "timestamp": datetime.now() - timedelta(days=1)
            }
        }
        
        # Test serialization
        serialized = serialize_datetime(test_data)
        print("✅ DateTime serialization successful")
        
        # Verify all datetime objects are now strings
        for key, value in serialized.items():
            if key in ['created_at', 'updated_at']:
                if isinstance(value, str):
                    print(f"   ✅ {key}: {value[:20]}... (converted to string)")
                else:
                    print(f"   ❌ {key}: {type(value)} (still datetime)")
                    return False
        
        # Test profile data cleaning
        cleaned_profile = clean_profile_data(test_data)
        print("✅ Profile data cleaning successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing datetime serialization: {e}")
        return False

def test_auth_service():
    """Test if auth service can handle datetime objects properly"""
    
    print("\n🔐 Testing Auth Service...")
    
    try:
        from app.services.auth_service import auth_service
        from datetime import datetime
        
        if auth_service.supabase:
            print("✅ Auth service initialized successfully")
            
            # Test if we can get user profile without datetime errors
            try:
                # This should not raise datetime serialization errors
                response = auth_service.supabase.table('profiles').select('*').limit(1).execute()
                
                if response.data:
                    print("✅ Database query successful")
                    
                    # Test profile cleaning
                    from app.core.utils import clean_profile_data
                    cleaned = clean_profile_data(response.data[0])
                    print("✅ Profile cleaning successful")
                    
                    # Verify no datetime objects remain
                    for key, value in cleaned.items():
                        if isinstance(value, datetime):
                            print(f"   ❌ {key}: {type(value)} (still datetime)")
                            return False
                    
                    print("✅ All datetime objects properly serialized")
                    return True
                else:
                    print("⚠️  No profile data found to test")
                    return True
                    
            except Exception as e:
                print(f"❌ Database query failed: {e}")
                return False
        else:
            print("❌ Auth service not initialized")
            return False
            
    except Exception as e:
        print(f"❌ Error testing auth service: {e}")
        return False

def test_json_serialization():
    """Test if cleaned data can be properly serialized to JSON"""
    
    print("\n📄 Testing JSON Serialization...")
    
    try:
        import json
        from app.core.utils import clean_profile_data
        from datetime import datetime
        
        # Create test profile data
        test_profile = {
            "id": "test-123",
            "email": "test@example.com",
            "full_name": "Test User",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        # Clean the profile data
        cleaned = clean_profile_data(test_profile)
        
        # Try to serialize to JSON
        json_str = json.dumps(cleaned)
        print("✅ JSON serialization successful")
        
        # Verify the JSON string contains the expected data
        if "test@example.com" in json_str and "Test User" in json_str:
            print("✅ JSON contains expected data")
            return True
        else:
            print("❌ JSON missing expected data")
            return False
            
    except Exception as e:
        print(f"❌ Error testing JSON serialization: {e}")
        return False

def main():
    """Main test function"""
    
    print("🚀 CTAS AI DateTime Serialization Fix Test")
    print("=" * 60)
    
    # Test datetime serialization utilities
    success1 = test_datetime_serialization()
    
    print("\n" + "=" * 60)
    
    # Test auth service
    success2 = test_auth_service()
    
    print("\n" + "=" * 60)
    
    # Test JSON serialization
    success3 = test_json_serialization()
    
    print("\n" + "=" * 60)
    
    if success1 and success2 and success3:
        print("🎉 DateTime serialization issue resolved successfully!")
        print("\nNext steps:")
        print("1. Your login endpoint should now work without datetime errors")
        print("2. All profile data will be properly serialized")
        print("3. You can test the login functionality")
    else:
        print("❌ DateTime serialization issue still exists")
        print("\nTroubleshooting steps:")
        print("1. Check that all utility functions are properly imported")
        print("2. Verify the auth service is using the utility functions")
        print("3. Test individual components")

if __name__ == "__main__":
    main()
