# backend/app/services/sms_service.py
import logging
import requests
import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from supabase import create_client, Client
from app.core.config import settings
from app.core.ssl_utils import configure_ssl, create_supabase_client_options
from app.core.utils import clean_profile_data, serialize_datetime

logger = logging.getLogger(__name__)

class SMSService:
    def __init__(self):
        """Initialize SMS service with configuration"""
        # Configure SSL settings first
        configure_ssl()
        
        # Use settings from config
        self.supabase_url = settings.SUPABASE_URL
        self.supabase_key = settings.SUPABASE_KEY
        
        # Initialize Supabase client
        if self.supabase_url and self.supabase_key:
            try:
                # Get SSL options for Supabase client
                ssl_options = create_supabase_client_options()
                
                # Create client with SSL options
                self.supabase: Client = create_client(
                    self.supabase_url, 
                    self.supabase_key,
                    **ssl_options
                )
                logger.info("Supabase client initialized successfully for SMS service")
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client for SMS service: {e}")
                # Try fallback without SSL verification
                try:
                    logger.info("Attempting fallback connection without SSL verification")
                    self.supabase: Client = create_client(
                        self.supabase_url, 
                        self.supabase_key
                    )
                    logger.info("Fallback connection successful for SMS service")
                except Exception as fallback_e:
                    logger.error(f"Fallback connection also failed for SMS service: {fallback_e}")
                    self.supabase = None
        else:
            logger.error("Supabase configuration not found for SMS service")
            self.supabase = None
        
        # SMS configuration from settings
        self.sms_api_key = settings.SMS_API_KEY
        self.sms_api_url = settings.SMS_API_URL
        
        # Default SMS provider (can be overridden)
        self.sms_provider = "twilio"  # Options: twilio, nexmo, aws_sns, custom
        
        logger.info(f"SMS service initialized - API Key: {'Configured' if self.sms_api_key else 'Not configured'}")

    def get_users_with_phone_numbers(self, location: Optional[str] = None) -> List[Dict]:
        """
        Get all users with valid phone numbers from the database
        
        Args:
            location: Optional location filter
            
        Returns:
            List of users with phone numbers
        """
        try:
            if not self.supabase:
                logger.error("Supabase client not initialized")
                return []
            
            # Build query
            query = self.supabase.table('profiles').select('*')
            
            # Add location filter if specified
            if location:
                query = query.eq('location', location)
            
            # Add phone number filter (only users with phone numbers)
            query = query.not_.is_('phone', 'null')
            
            response = query.execute()
            
            if response.data:
                # Filter users with valid phone numbers
                valid_users = []
                for user in response.data:
                    if user.get('phone') and self._is_valid_phone_number(user['phone']):
                        cleaned_user = clean_profile_data(user)
                        valid_users.append(cleaned_user)
                
                logger.info(f"Retrieved {len(valid_users)} users with valid phone numbers")
                return valid_users
            else:
                logger.warning("No users with phone numbers found in database")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching users with phone numbers: {e}")
            return []

    def _is_valid_phone_number(self, phone: str) -> bool:
        """
        Validate phone number format
        
        Args:
            phone: Phone number to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not phone:
            return False
        
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone)
        
        # Check if it's a valid length (7-15 digits)
        if len(digits_only) < 7 or len(digits_only) > 15:
            return False
        
        # Basic format validation
        phone_pattern = re.compile(r'^\+?[\d\s\-\(\)]+$')
        return bool(phone_pattern.match(phone))

    def _format_phone_number(self, phone: str) -> str:
        """
        Format phone number for SMS sending
        
        Args:
            phone: Raw phone number
            
        Returns:
            Formatted phone number
        """
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone)
        
        # Add country code if not present (assuming India +91)
        if len(digits_only) == 10:
            return f"+91{digits_only}"
        elif len(digits_only) == 12 and digits_only.startswith('91'):
            return f"+{digits_only}"
        elif len(digits_only) == 11 and digits_only.startswith('91'):
            return f"+{digits_only}"
        else:
            return f"+{digits_only}"

    def send_sms_alert(self, phone: str, message: str) -> Tuple[bool, str]:
        """
        Send SMS alert to a single phone number
        
        Args:
            phone: Phone number to send SMS to
            message: SMS message content
            
        Returns:
            Tuple of (success: bool, error_message: str)
        """
        try:
            if not self.sms_api_key or not self.sms_api_url:
                return False, "SMS API not configured"
            
            # Format phone number
            formatted_phone = self._format_phone_number(phone)
            
            # Validate phone number
            if not self._is_valid_phone_number(formatted_phone):
                return False, f"Invalid phone number format: {phone}"
            
            # Send SMS based on provider
            if self.sms_provider == "twilio":
                return self._send_via_twilio(formatted_phone, message)
            elif self.sms_provider == "nexmo":
                return self._send_via_nexmo(formatted_phone, message)
            elif self.sms_provider == "aws_sns":
                return self._send_via_aws_sns(formatted_phone, message)
            else:
                return self._send_via_custom_api(formatted_phone, message)
                
        except Exception as e:
            logger.error(f"Error sending SMS to {phone}: {e}")
            return False, str(e)

    def _send_via_twilio(self, phone: str, message: str) -> Tuple[bool, str]:
        """Send SMS via Twilio"""
        try:
            # Twilio API endpoint
            twilio_url = f"https://api.twilio.com/2010-04-01/Accounts/{self.sms_api_key}/Messages.json"
            
            # You'll need to set up Twilio credentials in your .env file
            # TWILIO_ACCOUNT_SID=your_account_sid
            # TWILIO_AUTH_TOKEN=your_auth_token
            # TWILIO_PHONE_NUMBER=your_twilio_phone_number
            
            payload = {
                "To": phone,
                "From": settings.TWILIO_PHONE_NUMBER,
                "Body": message
            }
            
            response = requests.post(
                twilio_url,
                data=payload,
                auth=(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN),
                timeout=10
            )
            
            if response.status_code == 201:
                logger.info(f"Twilio SMS sent successfully to {phone}")
                return True, "SMS sent successfully"
            else:
                logger.error(f"Twilio API error: {response.status_code} - {response.text}")
                return False, f"Twilio API error: {response.status_code}"
                
        except Exception as e:
            logger.error(f"Twilio SMS error: {e}")
            return False, str(e)

    def _send_via_nexmo(self, phone: str, message: str) -> Tuple[bool, str]:
        """Send SMS via Nexmo (Vonage)"""
        try:
            # Nexmo API endpoint
            nexmo_url = "https://rest.nexmo.com/sms/json"
            
            payload = {
                "api_key": settings.NEXMO_API_KEY,
                "api_secret": settings.NEXMO_API_SECRET,
                "to": phone,
                "from": settings.NEXMO_PHONE_NUMBER,
                "text": message
            }
            
            response = requests.post(nexmo_url, data=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('messages', [{}])[0].get('status') == '0':
                    logger.info(f"Nexmo SMS sent successfully to {phone}")
                    return True, "SMS sent successfully"
                else:
                    error_msg = result.get('messages', [{}])[0].get('error-text', 'Unknown error')
                    logger.error(f"Nexmo SMS error: {error_msg}")
                    return False, error_msg
            else:
                logger.error(f"Nexmo API error: {response.status_code} - {response.text}")
                return False, f"Nexmo API error: {response.status_code}"
                
        except Exception as e:
            logger.error(f"Nexmo SMS error: {e}")
            return False, str(e)

    def _send_via_aws_sns(self, phone: str, message: str) -> Tuple[bool, str]:
        """Send SMS via AWS SNS"""
        try:
            # AWS SNS API endpoint
            sns_url = "https://sns.us-east-1.amazonaws.com/"
            
            payload = {
                "Action": "Publish",
                "Version": "2010-03-31",
                "PhoneNumber": phone,
                "Message": message
            }
            
            # You'll need to set up AWS credentials
            # AWS_ACCESS_KEY_ID=your_access_key
            # AWS_SECRET_ACCESS_KEY=your_secret_key
            # AWS_REGION=your_region
            
            response = requests.post(
                sns_url,
                data=payload,
                headers={
                    "Authorization": f"AWS4-HMAC-SHA256 Credential={settings.AWS_ACCESS_KEY_ID}",
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"AWS SNS SMS sent successfully to {phone}")
                return True, "SMS sent successfully"
            else:
                logger.error(f"AWS SNS API error: {response.status_code} - {response.text}")
                return False, f"AWS SNS API error: {response.status_code}"
                
        except Exception as e:
            logger.error(f"AWS SNS SMS error: {e}")
            return False, str(e)

    def _send_via_custom_api(self, phone: str, message: str) -> Tuple[bool, str]:
        """Send SMS via custom API"""
        try:
            payload = {
                "api_key": self.sms_api_key,
                "to": phone,
                "message": message,
                "sender": "CTAS"  # Custom sender ID
            }
            
            response = requests.post(self.sms_api_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"Custom API SMS sent successfully to {phone}")
                return True, "SMS sent successfully"
            else:
                logger.error(f"Custom SMS API error: {response.status_code} - {response.text}")
                return False, f"Custom SMS API error: {response.status_code}"
                
        except Exception as e:
            logger.error(f"Custom SMS API error: {e}")
            return False, str(e)

    def send_bulk_sms_alert(self, users: List[Dict], message: str) -> Dict:
        """
        Send SMS alerts to multiple users
        
        Args:
            users: List of user dictionaries with phone numbers
            message: SMS message content
            
        Returns:
            Dictionary with results summary
        """
        results = {
            "total_users": len(users),
            "successful": 0,
            "failed": 0,
            "errors": [],
            "timestamp": datetime.now().isoformat()
        }
        
        for user in users:
            phone = user.get('phone')
            if not phone:
                results["failed"] += 1
                results["errors"].append(f"No phone number for user {user.get('email', 'Unknown')}")
                continue
            
            success, error_msg = self.send_sms_alert(phone, message)
            
            if success:
                results["successful"] += 1
                logger.info(f"SMS sent successfully to {user.get('email', 'Unknown')} at {phone}")
            else:
                results["failed"] += 1
                results["errors"].append(f"Failed to send SMS to {user.get('email', 'Unknown')} at {phone}: {error_msg}")
        
        logger.info(f"Bulk SMS completed: {results['successful']} successful, {results['failed']} failed")
        return results

    def send_high_alert_sms(self, threat_level: str, threat_data: Dict, location: Optional[str] = None) -> Dict:
        """
        Send high alert SMS to all users with phone numbers
        
        Args:
            threat_level: Threat level (HIGH, MEDIUM, LOW)
            threat_data: Threat data dictionary
            location: Optional location filter
            
        Returns:
            Dictionary with results summary
        """
        try:
            # Get users with phone numbers
            users = self.get_users_with_phone_numbers(location)
            
            if not users:
                return {
                    "success": False,
                    "message": "No users with phone numbers found",
                    "total_users": 0,
                    "successful": 0,
                    "failed": 0
                }
            
            # Create SMS message
            sms_message = self._create_high_alert_message(threat_level, threat_data)
            
            # Send bulk SMS
            results = self.send_bulk_sms_alert(users, sms_message)
            
            # Store notification record
            self._store_sms_notification_record(threat_level, threat_data, results)
            
            return {
                "success": True,
                "message": f"SMS alerts sent to {results['successful']} users",
                **results
            }
            
        except Exception as e:
            logger.error(f"Error sending high alert SMS: {e}")
            return {
                "success": False,
                "message": f"Error sending SMS alerts: {str(e)}",
                "total_users": 0,
                "successful": 0,
                "failed": 0
            }

    def _create_high_alert_message(self, threat_level: str, threat_data: Dict) -> str:
        """
        Create SMS message for high alert
        
        Args:
            threat_level: Threat level
            threat_data: Threat data
            
        Returns:
            Formatted SMS message
        """
        cyclone_data = threat_data.get('cyclone', {})
        surge_data = threat_data.get('storm_surge', {})
        
        message = f"""🚨 COASTAL THREAT ALERT 🚨
Level: {threat_level}
Time: {datetime.now().strftime('%H:%M')}

⚠️ IMMEDIATE ACTION REQUIRED
- Evacuate to higher ground
- Follow emergency instructions
- Take essential items only

Emergency: 911
CTAS Alert System

Cyclone Probability: {cyclone_data.get('probability', 0)*100:.1f}%
Storm Surge: {surge_data.get('threat_level', 'Unknown')}"""
        
        return message

    def _store_sms_notification_record(self, threat_level: str, threat_data: Dict, results: Dict) -> None:
        """
        Store SMS notification record in database
        
        Args:
            threat_level: Threat level
            threat_data: Threat data
            results: SMS results
        """
        try:
            if not self.supabase:
                logger.warning("Supabase not available, skipping SMS notification record storage")
                return
            
            notification_record = {
                "timestamp": datetime.now().isoformat(),
                "threat_level": threat_level,
                "threat_type": "sms_alert",
                "total_users": results["total_users"],
                "sms_sent": results["successful"],
                "failed": results["failed"],
                "threat_data": threat_data,
                "results": results
            }
            
            # Store in notifications table
            response = self.supabase.table('notifications').insert(notification_record).execute()
            
            if response.data:
                logger.info("SMS notification record stored in database")
            else:
                logger.warning("Failed to store SMS notification record")
                
        except Exception as e:
            logger.error(f"Error storing SMS notification record: {e}")

# Create a global instance
sms_service = SMSService()
