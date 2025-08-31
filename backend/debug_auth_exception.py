#!/usr/bin/env python3
"""
Debug script to see the exact exception during auth signup
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

def debug_auth_exception():
    """Debug the exact exception during auth signup"""
    
    try:
        from app.services.auth_service import auth_service
        
        print("🔍 Debugging auth signup exception...")
        
        if auth_service.supabase:
            print("✅ Supabase client initialized successfully")
            
            # Test just the Supabase auth signup part
            test_email = "sutariyanaitik8@gmail.com"
            test_password = "testpassword123"
            
            print(f"\nTesting Supabase auth signup for: {test_email}")
            
            try:
                # This is the exact line that might be failing
                auth_response = auth_service.supabase.auth.sign_up({
                    "email": test_email,
                    "password": test_password
                })
                
                print(f"   Auth response: {auth_response}")
                print(f"   Auth response type: {type(auth_response)}")
                
                if hasattr(auth_response, 'user'):
                    print(f"   User created: {auth_response.user}")
                else:
                    print("   No user in response")
                    
            except Exception as e:
                print(f"   ❌ Exception during auth signup: {e}")
                print(f"   Exception type: {type(e)}")
                print(f"   Exception args: {e.args}")
                
                # Check if it's a Supabase-specific error
                if hasattr(e, 'code'):
                    print(f"   Error code: {e.code}")
                if hasattr(e, 'message'):
                    print(f"   Error message: {e.message}")
                if hasattr(e, 'details'):
                    print(f"   Error details: {e.details}")
                    
                import traceback
                traceback.print_exc()
                
        else:
            print("❌ Supabase client failed to initialize")
            
    except Exception as e:
        print(f"❌ Error in debug script: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_auth_exception()
