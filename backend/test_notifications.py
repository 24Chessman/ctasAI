#!/usr/bin/env python3
"""
Test script for manually testing the notification system
Run this script to test different notification scenarios
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

from app.services.notification_service import notification_service
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_notification_service():
    """Test the notification service with sample data"""
    
    print("🧪 Testing Notification Service...")
    print("=" * 50)
    
    # Test 1: Get all users
    print("\n1. Testing user retrieval...")
    users = notification_service.get_all_users()
    print(f"   Found {len(users)} users in database")
    
    if users:
        print("   Sample user data:")
        for i, user in enumerate(users[:3]):  # Show first 3 users
            print(f"   User {i+1}: {user.get('email', 'No email')} | {user.get('phone', 'No phone')}")
    
    # Test 2: Test evacuation alert with high threat
    print("\n2. Testing evacuation alert (HIGH threat)...")
    
    # Sample threat data that would trigger evacuation
    high_threat_data = {
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
    result = notification_service.send_evacuation_alert(high_threat_data)
    
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
    
    # Test 3: Test evacuation alert with low threat (should not trigger)
    print("\n3. Testing evacuation alert (LOW threat)...")
    
    low_threat_data = {
        "overall_threat": "LOW",
        "cyclone": {
            "classification": "NO_CYCLONE",
            "probability": 0.2,
            "wind_speed": 25,
            "pressure": 1013
        },
        "storm_surge": {
            "threat_level": "low",
            "total_water_level": 0.5,
            "surge_height": 0.1,
            "tide_height": 0.4
        },
        "timestamp": "2024-01-15T14:30:00Z"
    }
    
    result = notification_service.send_evacuation_alert(low_threat_data)
    print(f"   Low threat alert result: {result['success']}")
    print(f"   Message: {result['message']}")
    
    # Test 4: Test location-based user retrieval
    print("\n4. Testing location-based user retrieval...")
    # You can modify this location based on your database
    location_users = notification_service.get_users_by_location("coastal_zone_1")
    print(f"   Users in coastal_zone_1: {len(location_users)}")
    
    print("\n✅ Notification service testing completed!")
    print("\n📝 Notes:")
    print("   - Check your email inbox for notifications")
    print("   - Check console logs for detailed results")
    print("   - Verify database records in notifications table")

def test_alert_system():
    """Test the alert system integration"""
    
    print("\n🚨 Testing Alert System Integration...")
    print("=" * 50)
    
    # Import alert system
    from app.services.alert_system import check_and_send_alerts
    
    # Test data that should trigger alerts
    test_prediction = {
        "overall_threat": "HIGH",
        "cyclone": {
            "classification": "CYCLONE",
            "probability": 0.8,
            "wind_speed": 110,
            "pressure": 960
        },
        "storm_surge": {
            "threat_level": "high",
            "total_water_level": 2.8,
            "surge_height": 2.1,
            "tide_height": 0.7
        }
    }
    
    test_weather_data = {
        "wind_speed": 110,
        "pressure": 960,
        "temperature": 25,
        "humidity": 85
    }
    
    print("   Triggering alert system with high threat data...")
    check_and_send_alerts(test_prediction, test_weather_data)
    print("   Alert system check completed!")

if __name__ == "__main__":
    try:
        # Test notification service
        test_notification_service()
        
        # Test alert system
        test_alert_system()
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
