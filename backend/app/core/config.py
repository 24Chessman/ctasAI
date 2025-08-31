from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "CTAS AI - Coastal Threat Alert System"
    
    # Supabase Configuration
    SUPABASE_URL: str = "https://bdxchhewjbfzydeyjces.supabase.co"
    SUPABASE_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJkeGNoaGV3amJmenlkZXlqY2VzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTY1MDA1NTUsImV4cCI6MjA3MjA3NjU1NX0.t58O9RpsmRPv7_5jJFSxJkzHX2hIt0jsgrFXUHGOSb0"
    
    # SSL Configuration for handling certificate issues
    SSL_VERIFY: bool = True
    SSL_CERT_PATH: str = ""
    SSL_DISABLE_WARNING: bool = False
    
    # Email Configuration (for notifications)
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    
    # SMS Configuration (optional)
    SMS_API_KEY: str = ""
    SMS_API_URL: str = ""
    
    # Twilio SMS Configuration
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    
    # Nexmo (Vonage) SMS Configuration
    NEXMO_API_KEY: str = ""
    NEXMO_API_SECRET: str = ""
    NEXMO_PHONE_NUMBER: str = ""
    
    # AWS SNS Configuration
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    
    # Push Notification Configuration (optional)
    PUSH_API_KEY: str = ""
    PUSH_API_URL: str = ""
    
    # Weather API Keys
    STORMGLASS_API_KEY: str = ""
    NOAA_API_KEY: str = ""
    WEATHERAPI_API_KEY: str = ""
    OPENWEATHERMAP_API_KEY: str = ""
    WORLDTIDE_API_KEY: str = ""
    
    # Default coordinates
    DEFAULT_LATITUDE: str = "19.0760"
    DEFAULT_LONGITUDE: str = "72.8777"
    
    # Debug and logging
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # API settings
    API_V1_STR: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # Allow extra fields from environment variables
        extra = "allow"

# Create settings instance
settings = Settings()

# Override with environment variables if they exist
if os.getenv("SUPABASE_URL"):
    settings.SUPABASE_URL = os.getenv("SUPABASE_URL")
if os.getenv("SUPABASE_KEY"):
    settings.SUPABASE_KEY = os.getenv("SUPABASE_KEY")
if os.getenv("SSL_VERIFY"):
    settings.SSL_VERIFY = os.getenv("SSL_VERIFY").lower() == "true"
if os.getenv("SSL_CERT_PATH"):
    settings.SSL_CERT_PATH = os.getenv("SSL_CERT_PATH")
if os.getenv("SSL_DISABLE_WARNING"):
    settings.SSL_DISABLE_WARNING = os.getenv("SSL_DISABLE_WARNING").lower() == "true"
if os.getenv("SMTP_USERNAME"):
    settings.SMTP_USERNAME = os.getenv("SMTP_USERNAME")
if os.getenv("SMTP_PASSWORD"):
    settings.SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
if os.getenv("SMS_API_KEY"):
    settings.SMS_API_KEY = os.getenv("SMS_API_KEY")
if os.getenv("SMS_API_URL"):
    settings.SMS_API_URL = os.getenv("SMS_API_URL")
if os.getenv("TWILIO_ACCOUNT_SID"):
    settings.TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
if os.getenv("TWILIO_AUTH_TOKEN"):
    settings.TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
if os.getenv("TWILIO_PHONE_NUMBER"):
    settings.TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
if os.getenv("NEXMO_API_KEY"):
    settings.NEXMO_API_KEY = os.getenv("NEXMO_API_KEY")
if os.getenv("NEXMO_API_SECRET"):
    settings.NEXMO_API_SECRET = os.getenv("NEXMO_API_SECRET")
if os.getenv("NEXMO_PHONE_NUMBER"):
    settings.NEXMO_PHONE_NUMBER = os.getenv("NEXMO_PHONE_NUMBER")
if os.getenv("AWS_ACCESS_KEY_ID"):
    settings.AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
if os.getenv("AWS_SECRET_ACCESS_KEY"):
    settings.AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
if os.getenv("AWS_REGION"):
    settings.AWS_REGION = os.getenv("AWS_REGION")
if os.getenv("PUSH_API_KEY"):
    settings.PUSH_API_KEY = os.getenv("PUSH_API_KEY")
if os.getenv("PUSH_API_URL"):
    settings.PUSH_API_URL = os.getenv("PUSH_API_URL")