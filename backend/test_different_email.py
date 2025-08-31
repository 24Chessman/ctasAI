#!/usr/bin/env python3
"""
Test registration with a completely different email
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

def test_different_email():
    """Test registration with a different email"""
    
    try:
        from app.services.auth_service import auth_service
        
        print("🔍 Testing registration with different email...")
        
        if auth_service.supabase:
            print("✅ Supabase client initialized successfully")
            
            # Test with a completely different email
            test_data = {
                "email": "completelynewuser@test.com",
                "password": "testpassword123",
                "full_name": "Test User",
                "phone": "1234567890",
                "location": "coastal_zone_1"
            }
            
            print(f"\nAttempting registration with:")
            print(f"   Email: {test_data['email']}")
            print(f"   Full Name: {test_data['full_name']}")
            
            try:
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
                
                if result.get('success'):
                    print("   ✅ Registration successful with different email!")
                    print("   This confirms the system works, but the original email has an auth conflict")
                else:
                    print("   ❌ Registration still failed with different email")
                    print(f"   Error: {result.get('message')}")
                    
            except Exception as e:
                print(f"   ❌ Exception: {e}")
                
        else:
            print("❌ Supabase client failed to initialize")
            
    except Exception as e:
        print(f"❌ Error in test script: {e}")

if __name__ == "__main__":
    test_different_email()
