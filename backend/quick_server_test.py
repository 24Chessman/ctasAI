#!/usr/bin/env python3
"""
Quick server test to check if backend is accessible
"""

import requests
import time

def test_server():
    """Test if server is accessible"""
    
    print("🔍 Testing server accessibility...")
    
    # Try different URLs
    urls = [
        "http://localhost:8000/docs",
        "http://127.0.0.1:8000/docs",
        "http://localhost:8000/",
        "http://127.0.0.1:8000/"
    ]
    
    for url in urls:
        try:
            print(f"   Trying: {url}")
            response = requests.get(url, timeout=3)
            print(f"   ✅ Success! Status: {response.status_code}")
            return True
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Connection failed")
        except requests.exceptions.Timeout:
            print(f"   ⏰ Timeout")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return False

def test_login_endpoint():
    """Test login endpoint specifically"""
    
    print("\n🔐 Testing login endpoint...")
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            headers={"Content-Type": "application/json"},
            json={"email": "test@example.com", "password": "test123"},
            timeout=5
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
        return response.status_code < 500  # Any response is good, even 401/400
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Quick Server Test")
    print("=" * 30)
    
    # Test server accessibility
    server_accessible = test_server()
    
    if server_accessible:
        print("\n✅ Server is accessible!")
        
        # Test login endpoint
        login_working = test_login_endpoint()
        
        if login_working:
            print("\n🎉 Login endpoint is working!")
            print("\nThe issue might be:")
            print("1. Frontend not connecting to correct URL")
            print("2. CORS issues")
            print("3. Network connectivity")
            print("4. Browser console errors")
        else:
            print("\n❌ Login endpoint has issues")
    else:
        print("\n❌ Server is not accessible")
        print("Make sure the server is running on port 8000")
