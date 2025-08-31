#!/usr/bin/env python3
"""
Test script to run the full registration process and see where it fails
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

def test_full_registration():
    """Test the full registration process"""
    
    try:
        from app.services.auth_service import auth_service
        
        print("🔍 Testing full registration process...")
        
        if auth_service.supabase:
            print("✅ Supabase client initialized successfully")
            
            # Test registration with the exact data from the form
            test_data = {
                "email": "sutariyanaitik8@gmail.com",
                "password": "testpassword123",
                "full_name": "Naitik Sutariya",
                "phone": "9327145977",
                "location": "coastal_zone_1"
            }
            
            print(f"\nAttempting registration with:")
            print(f"   Email: {test_data['email']}")
            print(f"   Full Name: {test_data['full_name']}")
            print(f"   Phone: {test_data['phone']}")
            print(f"   Location: {test_data['location']}")
            
            try:
                # Call the actual registration method
                result = auth_service.register_user(
                    email=test_data["email"],
                    password=test_data["password"],
                    full_name=test_data["full_name"],
                    phone=test_data["phone"],
                    location=test_data["location"]
                )
                
                print(f"\nRegistration result:")
                print(f"   Success: {result.get('success', 'Unknown')}")
                print(f"   Message: {result.get('message', 'No message')}")
                print(f"   User ID: {result.get('user_id', 'No ID')}")
                
                if result.get('success'):
                    print("   ✅ Registration successful!")
                else:
                    print("   ❌ Registration failed!")
                    print(f"   Error message: {result.get('message')}")
                    
            except Exception as e:
                print(f"   ❌ Exception during registration: {e}")
                import traceback
                traceback.print_exc()
                
        else:
            print("❌ Supabase client failed to initialize")
            
    except Exception as e:
        print(f"❌ Error in test script: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_full_registration()
