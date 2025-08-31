#!/usr/bin/env python3
"""
Debug script to test registration process step by step
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

def test_registration_debug():
    """Debug the registration process step by step"""
    
    try:
        from app.services.auth_service import auth_service
        
        print("🔍 Debugging registration process...")
        
        if auth_service.supabase:
            print("✅ Supabase client initialized successfully")
            
            # Test 1: Check what users currently exist
            print("\n1. Checking existing users...")
            try:
                existing_users = auth_service.supabase.table('profiles').select('*').execute()
                print(f"   Total users in database: {len(existing_users.data) if existing_users.data else 0}")
                
                if existing_users.data:
                    for user in existing_users.data:
                        print(f"   User: {user.get('email', 'NO_EMAIL')} | ID: {user.get('id', 'NO_ID')}")
                else:
                    print("   No users found in database")
                    
            except Exception as e:
                print(f"   ❌ Error checking existing users: {e}")
            
            # Test 2: Try to check if a specific email exists
            print("\n2. Testing email existence check...")
            test_email = "test@example.com"
            
            try:
                existing_user = auth_service.supabase.table('profiles').select('*').eq('email', test_email).execute()
                print(f"   Checking for email: {test_email}")
                print(f"   Found users: {len(existing_user.data) if existing_user.data else 0}")
                
                if existing_user.data:
                    print(f"   User data: {existing_user.data[0]}")
                else:
                    print("   No user found with this email")
                    
            except Exception as e:
                print(f"   ❌ Error checking email existence: {e}")
            
            # Test 3: Check if the auto-generated email exists
            print("\n3. Checking auto-generated email...")
            auto_email = "user_15e4f713-870e-4aee-9184-a52ec3258b5b@example.com"
            
            try:
                auto_user = auth_service.supabase.table('profiles').select('*').eq('email', auto_email).execute()
                print(f"   Checking for auto-generated email: {auto_email}")
                print(f"   Found users: {len(auto_user.data) if auto_user.data else 0}")
                
                if auto_user.data:
                    print(f"   Auto-generated user data: {auto_user.data[0]}")
                else:
                    print("   No auto-generated user found")
                    
            except Exception as e:
                print(f"   ❌ Error checking auto-generated email: {e}")
            
            # Test 4: Check table structure
            print("\n4. Checking table structure...")
            try:
                # Try to select specific columns
                test_select = auth_service.supabase.table('profiles').select('id, email, full_name, location, role').limit(1).execute()
                print(f"   Select test successful: {test_select.data}")
                
            except Exception as e:
                print(f"   ❌ Error in select test: {e}")
                
        else:
            print("❌ Supabase client failed to initialize")
            
    except Exception as e:
        print(f"❌ Error in debug script: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_registration_debug()
