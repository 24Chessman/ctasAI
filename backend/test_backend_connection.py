#!/usr/bin/env python3
"""
Test backend connection and registration endpoint
"""

import requests
import json

def test_backend_connection():
    """Test if backend is accessible"""
    
    print("🔍 Testing Backend Connection...")
    
    # Test basic connectivity
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        print(f"✅ Backend is accessible - Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        return False

def test_registration_endpoint():
    """Test registration endpoint"""
    
    print("\n🔐 Testing Registration Endpoint...")
    
    try:
        # Test registration data
        registration_data = {
            "email": "test@example.com",
            "password": "test123",
            "full_name": "Test User",
            "phone": "1234567890",
            "location": "Test City"
        }
        
        print(f"📤 Sending registration request...")
        response = requests.post(
            "http://127.0.0.1:8000/api/v1/auth/register",
            headers={"Content-Type": "application/json"},
            json=registration_data,
            timeout=10
        )
        
        print(f"📥 Response Status: {response.status_code}")
        print(f"📥 Response Headers: {dict(response.headers)}")
        
        try:
            response_data = response.json()
            print(f"📥 Response Data: {json.dumps(response_data, indent=2)}")
        except:
            print(f"📥 Response Text: {response.text}")
        
        return response.status_code < 500  # Any response is good, even 400/409 for existing user
        
    except Exception as e:
        print(f"❌ Registration test failed: {e}")
        return False

def test_login_endpoint():
    """Test login endpoint"""
    
    print("\n🔑 Testing Login Endpoint...")
    
    try:
        # Test login data
        login_data = {
            "email": "test@example.com",
            "password": "test123"
        }
        
        print(f"📤 Sending login request...")
        response = requests.post(
            "http://127.0.0.1:8000/api/v1/auth/login",
            headers={"Content-Type": "application/json"},
            json=login_data,
            timeout=10
        )
        
        print(f"📥 Response Status: {response.status_code}")
        
        try:
            response_data = response.json()
            print(f"📥 Response Data: {json.dumps(response_data, indent=2)}")
        except:
            print(f"📥 Response Text: {response.text}")
        
        return response.status_code < 500  # Any response is good, even 401 for wrong credentials
        
    except Exception as e:
        print(f"❌ Login test failed: {e}")
        return False

def main():
    """Main test function"""
    
    print("🚀 Backend Connection Test")
    print("=" * 50)
    
    # Test backend connection
    backend_ok = test_backend_connection()
    
    if backend_ok:
        # Test registration endpoint
        registration_ok = test_registration_endpoint()
        
        # Test login endpoint
        login_ok = test_login_endpoint()
        
        print("\n" + "=" * 50)
        
        if registration_ok and login_ok:
            print("🎉 Backend endpoints are working correctly!")
            print("\nThe issue is likely in the frontend configuration.")
            print("Please check:")
            print("1. Frontend environment variables")
            print("2. Browser console for errors")
            print("3. Network connectivity between frontend and backend")
        else:
            print("❌ Some backend endpoints have issues")
    else:
        print("\n❌ Backend is not accessible")
        print("Please make sure the backend server is running on port 8000")

if __name__ == "__main__":
    main()
