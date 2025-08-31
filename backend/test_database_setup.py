#!/usr/bin/env python3
"""
Comprehensive test script for the new database setup
Tests authentication, user management, and notification features
"""

import os
import sys
import requests
import json
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

def test_api_endpoints():
    """Test all API endpoints"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing API Endpoints...")
    print("=" * 50)
    
    # Test 1: Root endpoint
    print("\n1. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Root endpoint working: {data['message']}")
            print(f"   Available endpoints: {list(data['endpoints'].keys())}")
        else:
            print(f"   ❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error testing root endpoint: {e}")
    
    # Test 2: Health check
    print("\n2. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health check working: {data['status']}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error testing health check: {e}")
    
    # Test 3: Auth endpoints
    print("\n3. Testing authentication endpoints...")
    
    # Test registration
    test_user = {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User",
        "phone": "+1234567890",
        "location": "coastal_zone_1"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/v1/auth/register",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ User registration working: {data['message']}")
            user_id = data['data']['user_id']
        else:
            print(f"   ❌ User registration failed: {response.status_code} - {response.text}")
            user_id = None
    except Exception as e:
        print(f"   ❌ Error testing registration: {e}")
        user_id = None
    
    # Test login
    if user_id:
        try:
            login_data = {
                "email": test_user["email"],
                "password": test_user["password"]
            }
            
            response = requests.post(
                f"{base_url}/api/v1/auth/login",
                json=login_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ User login working: {data['message']}")
                access_token = data['data']['access_token']
            else:
                print(f"   ❌ User login failed: {response.status_code} - {response.text}")
                access_token = None
        except Exception as e:
            print(f"   ❌ Error testing login: {e}")
            access_token = None
    else:
        access_token = None
    
    # Test 4: Alerts endpoints
    print("\n4. Testing alerts endpoints...")
    
    try:
        response = requests.get(f"{base_url}/api/v1/alerts/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Alerts endpoint working: {data['message']}")
        else:
            print(f"   ❌ Alerts endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error testing alerts endpoint: {e}")
    
    # Test notification with test email
    if access_token:
        try:
            test_notification = {
                "threat_level": "HIGH",
                "cyclone_probability": 0.8,
                "storm_surge_level": "high",
                "water_level": 3.0,
                "test_email": test_user["email"]
            }
            
            response = requests.post(
                f"{base_url}/api/v1/alerts/test-notification",
                json=test_notification,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Test notification working: {data['message']}")
            else:
                print(f"   ❌ Test notification failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"   ❌ Error testing notification: {e}")
    
    # Test 5: Get users
    print("\n5. Testing user retrieval...")
    
    try:
        response = requests.get(f"{base_url}/api/v1/alerts/users")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ User retrieval working: Found {data['user_count']} users")
        else:
            print(f"   ❌ User retrieval failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error testing user retrieval: {e}")

def test_database_connection():
    """Test direct database connection"""
    
    print("\n🔌 Testing Database Connection...")
    print("=" * 50)
    
    try:
        from app.services.notification_service import notification_service
        
        # Test user retrieval
        users = notification_service.get_all_users()
        print(f"   ✅ Database connection working: Found {len(users)} users")
        
        if users:
            print("   Sample users:")
            for i, user in enumerate(users[:3]):
                print(f"   User {i+1}: {user.get('email', 'No email')} | {user.get('full_name', 'No name')}")
        
        # Test location-based user retrieval
        location_users = notification_service.get_users_by_location("coastal_zone_1")
        print(f"   Users in coastal_zone_1: {len(location_users)}")
        
    except Exception as e:
        print(f"   ❌ Database connection failed: {e}")
        import traceback
        traceback.print_exc()

def test_notification_service():
    """Test notification service directly"""
    
    print("\n📧 Testing Notification Service...")
    print("=" * 50)
    
    try:
        from app.services.notification_service import notification_service
        
        # Test threat data
        test_threat_data = {
            "overall_threat": "HIGH",
            "cyclone": {
                "classification": "CYCLONE",
                "probability": 0.85,
                "wind_speed": 120,
                "pressure": 950
            },
            "storm_surge": {
                "threat_level": "extreme",
                "total_water_level": 3.5,
                "surge_height": 2.8,
                "tide_height": 0.7
            },
            "timestamp": "2024-01-15T14:30:00Z"
        }
        
        # Send evacuation alert
        result = notification_service.send_evacuation_alert(test_threat_data)
        
        print(f"   Evacuation alert result: {result['success']}")
        if result['success']:
            print(f"   Message: {result['message']}")
            if 'results' in result:
                results = result['results']
                print(f"   Total users: {results['total_users']}")
                print(f"   Email sent: {results['email_sent']}")
                print(f"   SMS sent: {results['sms_sent']}")
                print(f"   Push sent: {results['push_sent']}")
                print(f"   Failed: {results['failed']}")
        else:
            print(f"   Error: {result['message']}")
            
    except Exception as e:
        print(f"   ❌ Notification service test failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main test function"""
    
    print("🚀 Starting Comprehensive Database and API Tests")
    print("=" * 60)
    
    # Check if backend is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend server is running")
        else:
            print("❌ Backend server is not responding correctly")
            return
    except requests.exceptions.RequestException:
        print("❌ Backend server is not running. Please start it first:")
        print("   cd backend")
        print("   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        return
    
    # Run tests
    test_api_endpoints()
    test_database_connection()
    test_notification_service()
    
    print("\n🎉 Testing completed!")
    print("\n📝 Next steps:")
    print("   1. Check your email for test notifications (if configured)")
    print("   2. Verify database records in Supabase dashboard")
    print("   3. Test the web dashboard: open backend/test_notifications.html")

if __name__ == "__main__":
    main()
