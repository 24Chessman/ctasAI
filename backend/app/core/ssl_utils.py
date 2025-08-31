"""
SSL Utility functions for handling certificate verification issues
"""
import os
import ssl
import urllib3
import warnings
from typing import Optional
from app.core.config import settings

def configure_ssl():
    """
    Configure SSL settings based on configuration
    """
    if not settings.SSL_VERIFY:
        # Disable SSL verification warnings
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Disable SSL verification for requests
        os.environ['CURL_CA_BUNDLE'] = ''
        os.environ['REQUESTS_CA_BUNDLE'] = ''
        
        # Set SSL context to not verify
        ssl._create_default_https_context = ssl._create_unverified_context
        
        print("⚠️  SSL verification disabled - this is not recommended for production")
    
    if settings.SSL_CERT_PATH and os.path.exists(settings.SSL_CERT_PATH):
        # Set custom certificate path
        os.environ['CURL_CA_BUNDLE'] = settings.SSL_CERT_PATH
        os.environ['REQUESTS_CA_BUNDLE'] = settings.SSL_CERT_PATH
        print(f"✅ Using custom SSL certificate: {settings.SSL_CERT_PATH}")
    
    if settings.SSL_DISABLE_WARNING:
        # Suppress SSL warnings
        warnings.filterwarnings('ignore', message='Unverified HTTPS request')
        print("⚠️  SSL warnings suppressed")

def get_ssl_context(verify: Optional[bool] = None) -> ssl.SSLContext:
    """
    Get SSL context with appropriate verification settings
    
    Args:
        verify: Override SSL verification setting
        
    Returns:
        Configured SSL context
    """
    if verify is None:
        verify = settings.SSL_VERIFY
    
    if verify:
        # Create default SSL context with verification
        context = ssl.create_default_context()
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        return context
    else:
        # Create unverified SSL context
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context

def create_supabase_client_options():
    """
    Create options for Supabase client to handle SSL issues
    
    Returns:
        Dictionary of options for Supabase client
    """
    options = {}
    
    # Note: Supabase Python client doesn't support verify parameter directly
    # SSL configuration is handled at the system level through configure_ssl()
    
    return options
