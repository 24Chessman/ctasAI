#!/usr/bin/env python3
"""
Test script to check if a specific email exists in the database
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

def test_specific_email():
    """Test if the specific email exists"""
    
    try:
        from app.services.auth_service import auth_service
        
        print("🔍 Testing specific email existence...")
        
        if auth_service.supabase:
            print("✅ Supabase client initialized successfully")
            
            # Test the specific email from the form
            test_email = "sutariyanaitik8@gmail.com"
            
            print(f"\nChecking for email: {test_email}")
            
            try:
                existing_user = auth_service.supabase.table('profiles').select('*').eq('email', test_email).execute()
                print(f"   Found users: {len(existing_user.data) if existing_user.data else 0}")
                
                if existing_user.data:
                    print(f"   User data: {existing_user.data[0]}")
                    print("   ❌ This email already exists in the database!")
                else:
                    print("   ✅ This email does NOT exist - registration should work!")
                    
            except Exception as e:
                print(f"   ❌ Error checking email existence: {e}")
            
            # Test with a completely new email
            new_test_email = "completelynew@example.com"
            print(f"\nChecking for completely new email: {new_test_email}")
            
            try:
                new_user = auth_service.supabase.table('profiles').select('*').eq('email', new_test_email).execute()
                print(f"   Found users: {len(new_user.data) if new_user.data else 0}")
                
                if new_user.data:
                    print(f"   ❌ Unexpected: This email exists!")
                else:
                    print("   ✅ This email does NOT exist - as expected")
                    
            except Exception as e:
                print(f"   ❌ Error checking new email: {e}")
                
        else:
            print("❌ Supabase client failed to initialize")
            
    except Exception as e:
        print(f"❌ Error in test script: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_specific_email()
