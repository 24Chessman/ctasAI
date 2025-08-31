#!/usr/bin/env python3
"""
Test script to verify SSL certificate fix
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

def test_ssl_configuration():
    """Test SSL configuration and Supabase connection"""
    
    print("🔒 Testing SSL Configuration...")
    
    try:
        # Import SSL utilities
        from app.core.ssl_utils import configure_ssl, create_supabase_client_options
        print("✅ SSL utilities imported successfully")
        
        # Configure SSL
        configure_ssl()
        print("✅ SSL configuration applied")
        
        # Test Supabase client creation
        from app.services.auth_service import auth_service
        
        if auth_service.supabase:
            print("✅ Supabase client created successfully with SSL configuration")
            
            # Test basic database query
            try:
                response = auth_service.supabase.table('profiles').select('*').limit(1).execute()
                print("✅ Database query successful - SSL issue resolved!")
                return True
            except Exception as e:
                print(f"❌ Database query failed: {e}")
                return False
        else:
            print("❌ Supabase client creation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing SSL configuration: {e}")
        return False

def test_environment_variables():
    """Test if SSL environment variables are set correctly"""
    
    print("\n🔧 Testing Environment Variables...")
    
    ssl_verify = os.getenv("SSL_VERIFY", "true")
    print(f"   SSL_VERIFY: {ssl_verify}")
    
    ssl_cert_path = os.getenv("SSL_CERT_PATH", "not set")
    print(f"   SSL_CERT_PATH: {ssl_cert_path}")
    
    ssl_disable_warning = os.getenv("SSL_DISABLE_WARNING", "false")
    print(f"   SSL_DISABLE_WARNING: {ssl_disable_warning}")
    
    if ssl_verify.lower() == "false":
        print("   ⚠️  SSL verification is disabled")
    else:
        print("   ✅ SSL verification is enabled")

def main():
    """Main test function"""
    
    print("🚀 CTAS AI SSL Certificate Fix Test")
    print("=" * 50)
    
    # Test environment variables
    test_environment_variables()
    
    print("\n" + "=" * 50)
    
    # Test SSL configuration
    success = test_ssl_configuration()
    
    print("\n" + "=" * 50)
    
    if success:
        print("🎉 SSL certificate issue resolved successfully!")
        print("\nNext steps:")
        print("1. Your backend should now connect to Supabase without SSL errors")
        print("2. You can start your backend server normally")
        print("3. Consider re-enabling SSL verification for production use")
    else:
        print("❌ SSL certificate issue still exists")
        print("\nTroubleshooting steps:")
        print("1. Check your .env file has SSL_VERIFY=false")
        print("2. Restart your backend server")
        print("3. Check the logs for specific error messages")
        print("4. Ensure urllib3 is installed: pip install urllib3")

if __name__ == "__main__":
    main()
