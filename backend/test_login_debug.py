#!/usr/bin/env python3
"""
Debug script to test login endpoint and identify issues
"""

import requests
import json
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

def test_backend_server():
    """Test if backend server is running"""
    try:
        response = requests.get("http://localhost:8000/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Backend server is running")
            return True
        else:
            print(f"❌ Backend server responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend server is not running")
        print("   Start the server with: python -m uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Error connecting to backend: {e}")
        return False

def test_login_endpoint():
    """Test the login endpoint"""
    try:
        # Test data
        login_data = {
            "email": "test@example.com",
            "password": "test123"
        }
        
        print("🔐 Testing login endpoint...")
        
        response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            headers={"Content-Type": "application/json"},
            json=login_data,
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response Headers: {dict(response.headers)}")
        
        try:
            response_data = response.json()
            print(f"   Response Body: {json.dumps(response_data, indent=2)}")
        except json.JSONDecodeError:
            print(f"   Response Text: {response.text}")
        
        if response.status_code == 200:
            print("✅ Login endpoint is working")
            return True
        else:
            print("❌ Login endpoint returned error")
            return False
            
    except Exception as e:
        print(f"❌ Error testing login endpoint: {e}")
        return False

def test_auth_service_directly():
    """Test auth service directly without HTTP"""
    try:
        print("\n🔧 Testing Auth Service directly...")
        
        from app.services.auth_service import auth_service
        
        if not auth_service.supabase:
            print("❌ Auth service not initialized")
            return False
        
        # Test login with auth service
        result = auth_service.login_user("test@example.com", "test123")
        
        print(f"   Auth Service Result: {result}")
        
        if result.get("success"):
            print("✅ Auth service login works")
            return True
        else:
            print(f"❌ Auth service login failed: {result.get('message')}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing auth service: {e}")
        return False

def check_environment():
    """Check environment configuration"""
    print("\n🔧 Checking Environment...")
    
    try:
        from app.core.config import settings
        
        print(f"   SUPABASE_URL: {'✅ Set' if settings.SUPABASE_URL else '❌ Not set'}")
        print(f"   SUPABASE_KEY: {'✅ Set' if settings.SUPABASE_KEY else '❌ Not set'}")
        print(f"   SSL_VERIFY: {settings.SSL_VERIFY}")
        
        # Test Supabase connection
        from app.services.auth_service import auth_service
        
        if auth_service.supabase:
            print("   Supabase Client: ✅ Initialized")
            
            # Test basic query
            try:
                response = auth_service.supabase.table('profiles').select('*').limit(1).execute()
                print("   Database Query: ✅ Working")
            except Exception as e:
                print(f"   Database Query: ❌ Failed - {e}")
        else:
            print("   Supabase Client: ❌ Not initialized")
            
    except Exception as e:
        print(f"   Environment Check: ❌ Error - {e}")

def main():
    """Main debug function"""
    
    print("🚀 CTAS AI Login Debug Test")
    print("=" * 50)
    
    # Check environment
    check_environment()
    
    print("\n" + "=" * 50)
    
    # Test backend server
    server_running = test_backend_server()
    
    if server_running:
        print("\n" + "=" * 50)
        
        # Test login endpoint
        endpoint_working = test_login_endpoint()
        
        print("\n" + "=" * 50)
        
        # Test auth service directly
        service_working = test_auth_service_directly()
        
        print("\n" + "=" * 50)
        
        # Summary
        if endpoint_working and service_working:
            print("🎉 Login system is working correctly!")
            print("\nPossible frontend issues:")
            print("1. Check browser console for JavaScript errors")
            print("2. Verify API_BASE_URL in frontend environment")
            print("3. Check CORS configuration")
            print("4. Verify network connectivity")
        else:
            print("❌ Login system has issues")
            print("\nTroubleshooting steps:")
            print("1. Check backend server logs")
            print("2. Verify Supabase configuration")
            print("3. Check database connection")
            print("4. Review environment variables")
    else:
        print("\n❌ Backend server is not running")
        print("Start the server with: python -m uvicorn app.main:app --reload")

if __name__ == "__main__":
    main()
