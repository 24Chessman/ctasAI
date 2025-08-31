#!/usr/bin/env python3
"""
Debug script to trace the exact registration flow
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

def debug_registration_flow():
    """Debug the exact registration flow step by step"""
    
    try:
        from app.services.auth_service import auth_service
        
        print("🔍 Debugging registration flow step by step...")
        
        if auth_service.supabase:
            print("✅ Supabase client initialized successfully")
            
            # Test the exact flow from the registration form
            test_email = "sutariyanaitik8@gmail.com"
            
            print(f"\n1. Testing email existence check for: {test_email}")
            
            try:
                # This is the exact line from auth_service.py
                existing_user = auth_service.supabase.table('profiles').select('*').eq('email', test_email).execute()
                
                print(f"   existing_user object type: {type(existing_user)}")
                print(f"   existing_user.data: {existing_user.data}")
                print(f"   existing_user.data type: {type(existing_user.data)}")
                print(f"   len(existing_user.data): {len(existing_user.data) if existing_user.data else 'N/A'}")
                print(f"   existing_user.data is None: {existing_user.data is None}")
                print(f"   existing_user.data == []: {existing_user.data == []}")
                print(f"   bool(existing_user.data): {bool(existing_user.data)}")
                
                # This is the exact condition from auth_service.py
                if existing_user.data:
                    print("   ❌ Condition 'if existing_user.data:' is TRUE - User exists!")
                    print("   This will cause 'User with this email already exists' error")
                else:
                    print("   ✅ Condition 'if existing_user.data:' is FALSE - User does NOT exist!")
                    print("   Registration should proceed to next step")
                    
            except Exception as e:
                print(f"   ❌ Error in email existence check: {e}")
            
            # Test with a completely new email
            new_test_email = "brandnew@example.com"
            print(f"\n2. Testing with completely new email: {new_test_email}")
            
            try:
                new_user = auth_service.supabase.table('profiles').select('*').eq('email', new_test_email).execute()
                
                print(f"   new_user.data: {new_user.data}")
                print(f"   bool(new_user.data): {bool(new_user.data)}")
                
                if new_user.data:
                    print("   ❌ Unexpected: New email shows as existing!")
                else:
                    print("   ✅ New email correctly shows as not existing")
                    
            except Exception as e:
                print(f"   ❌ Error checking new email: {e}")
                
        else:
            print("❌ Supabase client failed to initialize")
            
    except Exception as e:
        print(f"❌ Error in debug script: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_registration_flow()
