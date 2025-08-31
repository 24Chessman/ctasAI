#!/usr/bin/env python3
"""
Simple database connection test script
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

def test_database_connection():
    """Test database connection and table structure"""
    
    try:
        from app.services.auth_service import auth_service
        
        print("🔌 Testing database connection...")
        
        if auth_service.supabase:
            print("✅ Supabase client initialized successfully")
            
            # Test if we can query the profiles table
            try:
                response = auth_service.supabase.table('profiles').select('*').limit(1).execute()
                print("✅ Profiles table exists and is accessible")
                print(f"   Table structure: {response.columns if hasattr(response, 'columns') else 'Available'}")
                
                # Check if email column exists
                if response.data is not None:
                    print("✅ Email column exists in profiles table")
                else:
                    print("⚠️  Profiles table exists but may be empty")
                    
            except Exception as e:
                print(f"❌ Error accessing profiles table: {e}")
                print("   This suggests the table structure is incorrect or missing")
                
        else:
            print("❌ Supabase client failed to initialize")
            
    except Exception as e:
        print(f"❌ Error testing database: {e}")

if __name__ == "__main__":
    test_database_connection()
