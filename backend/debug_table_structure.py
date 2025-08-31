#!/usr/bin/env python3
"""
Debug script to check the exact table structure
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

def debug_table_structure():
    """Debug the exact table structure"""
    
    try:
        from app.services.auth_service import auth_service
        
        print("🔍 Debugging table structure...")
        
        if auth_service.supabase:
            print("✅ Supabase client initialized successfully")
            
            # Test 1: Check if profiles table exists
            try:
                response = auth_service.supabase.table('profiles').select('*').limit(1).execute()
                print("✅ Profiles table exists")
                print(f"   Response type: {type(response)}")
                print(f"   Response data: {response.data}")
                
                # Test 2: Try to get table info
                try:
                    # Try to get column information
                    info_response = auth_service.supabase.rpc('get_table_info', {'table_name': 'profiles'}).execute()
                    print(f"   Table info: {info_response.data}")
                except:
                    print("   Could not get table info via RPC")
                
                # Test 3: Try different column names
                print("\n🔍 Testing different column names...")
                
                # Test with 'email'
                try:
                    test1 = auth_service.supabase.table('profiles').select('email').limit(1).execute()
                    print("   ✅ 'email' column exists")
                except Exception as e:
                    print(f"   ❌ 'email' column error: {e}")
                
                # Test with 'Email'
                try:
                    test2 = auth_service.supabase.table('profiles').select('Email').limit(1).execute()
                    print("   ✅ 'Email' column exists")
                except Exception as e:
                    print(f"   ❌ 'Email' column error: {e}")
                
                # Test with 'EMAIL'
                try:
                    test3 = auth_service.supabase.table('profiles').select('EMAIL').limit(1).execute()
                    print("   ✅ 'EMAIL' column exists")
                except Exception as e:
                    print(f"   ❌ 'EMAIL' column error: {e}")
                
                # Test 4: Try to get all columns
                try:
                    all_cols = auth_service.supabase.table('profiles').select('*').limit(0).execute()
                    print(f"   All columns response: {all_cols}")
                except Exception as e:
                    print(f"   ❌ Error getting all columns: {e}")
                    
            except Exception as e:
                print(f"❌ Error accessing profiles table: {e}")
                print(f"   Error type: {type(e)}")
                print(f"   Error details: {str(e)}")
                
        else:
            print("❌ Supabase client failed to initialize")
            
    except Exception as e:
        print(f"❌ Error in debug script: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_table_structure()
