# backend/app/services/notification_service.py
import logging
import os
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict, Optional
from supabase import create_client, Client
from app.core.config import settings
from app.core.ssl_utils import configure_ssl, create_supabase_client_options
from app.core.utils import clean_profile_data, serialize_datetime

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        """Initialize notification service with configuration"""
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
                logger.info("Supabase client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
                # Try fallback without SSL verification
                try:
                    logger.info("Attempting fallback connection without SSL verification")
                    self.supabase: Client = create_client(
                        self.supabase_url, 
                        self.supabase_key
                    )
                    logger.info("Fallback connection successful")
                except Exception as fallback_e:
                    logger.error(f"Fallback connection also failed: {fallback_e}")
                    self.supabase = None
        else:
            logger.error("Supabase configuration not found")
            self.supabase = None
        
        # Email configuration from settings
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        
        # SMS configuration from settings
        self.sms_api_key = settings.SMS_API_KEY
        self.sms_api_url = settings.SMS_API_URL
        
        # Push notification configuration from settings
        self.push_api_key = settings.PUSH_API_KEY
        self.push_api_url = settings.PUSH_API_URL
        
        logger.info(f"Notification service initialized - Email: {'Configured' if self.smtp_username else 'Not configured'}, SMS: {'Configured' if self.sms_api_key else 'Not configured'}, Push: {'Configured' if self.push_api_key else 'Not configured'}")

    def get_all_users(self) -> List[Dict]:
        """
        Get all registered users from the database
        """
        try:
            if not self.supabase:
                logger.error("Supabase client not initialized")
                return []
            
            # Fetch users from profiles table
            response = self.supabase.table('profiles').select('*').execute()
            
            if response.data:
                logger.info(f"Retrieved {len(response.data)} users")
                # Clean profile data to avoid datetime serialization issues
                cleaned_users = [clean_profile_data(user) for user in response.data]
                return cleaned_users
            else:
                logger.warning("No users found in database")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching users: {e}")
            return []

    def get_users_by_location(self, location: str) -> List[Dict]:
        """
        Get users by specific location/zone
        """
        try:
            if not self.supabase:
                return []
            
            # Use the custom function to get users by zone
            response = self.supabase.rpc('get_users_by_zone', {'zone_name_param': location}).execute()
            
            if response.data:
                logger.info(f"Retrieved {len(response.data)} users from location: {location}")
                # Clean profile data to avoid datetime serialization issues
                cleaned_users = [clean_profile_data(user) for user in response.data]
                return cleaned_users
            else:
                logger.warning(f"No users found in location: {location}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching users by location: {e}")
            return []

    def send_evacuation_alert(self, threat_data: Dict, target_users: Optional[List[Dict]] = None) -> Dict:
        """
        Send evacuation alert to users
        """
        try:
            # Get users if not provided
            if target_users is None:
                target_users = self.get_all_users()
            
            if not target_users:
                logger.warning("No users to send evacuation alert to")
                return {"success": False, "message": "No users found", "sent_count": 0}
            
            # Prepare evacuation message
            evacuation_message = self._prepare_evacuation_message(threat_data)
            
            # Track notification results
            results = {
                "total_users": len(target_users),
                "email_sent": 0,
                "sms_sent": 0,
                "push_sent": 0,
                "failed": 0,
                "errors": []
            }
            
            # Send notifications to each user
            for user in target_users:
                try:
                    # Send email notification
                    if user.get('email'):
                        if self._send_email_notification(user['email'], evacuation_message):
                            results["email_sent"] += 1
                        else:
                            results["failed"] += 1
                    
                    # Send SMS notification (if phone number available)
                    if user.get('phone'):
                        if self._send_sms_notification(user['phone'], evacuation_message['sms_text']):
                            results["sms_sent"] += 1
                        else:
                            results["failed"] += 1
                    
                    # Send push notification (if device token available)
                    if user.get('device_token'):
                        if self._send_push_notification(user['device_token'], evacuation_message):
                            results["push_sent"] += 1
                        else:
                            results["failed"] += 1
                            
                except Exception as e:
                    results["failed"] += 1
                    results["errors"].append(f"User {user.get('id', 'unknown')}: {str(e)}")
                    logger.error(f"Error sending notification to user {user.get('id')}: {e}")
            
            # Log results
            total_sent = results["email_sent"] + results["sms_sent"] + results["push_sent"]
            logger.info(f"Evacuation alert sent: {total_sent} notifications, {results['failed']} failed")
            
            # Store notification record in database
            self._store_notification_record(threat_data, results)
            
            return {
                "success": True,
                "message": f"Evacuation alert sent to {total_sent} users",
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Error sending evacuation alert: {e}")
            return {"success": False, "message": str(e), "sent_count": 0}

    def _prepare_evacuation_message(self, threat_data: Dict) -> Dict:
        """
        Prepare evacuation message for different channels
        """
        threat_level = threat_data.get('overall_threat', 'UNKNOWN')
        cyclone_data = threat_data.get('cyclone', {})
        surge_data = threat_data.get('storm_surge', {})
        
        # Prepare different message formats
        email_subject = f"🚨 URGENT: Coastal Evacuation Alert - {threat_level} Threat Level"
        
        email_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 2px solid #ff4444; border-radius: 10px;">
                <h1 style="color: #ff4444; text-align: center;">🚨 COASTAL EVACUATION ALERT 🚨</h1>
                
                <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h2 style="color: #856404; margin-top: 0;">Threat Level: {threat_level}</h2>
                    <p style="margin-bottom: 0;"><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                
                <div style="background-color: #f8d7da; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="color: #721c24; margin-top: 0;">⚠️ IMMEDIATE ACTION REQUIRED</h3>
                    <ul style="color: #721c24;">
                        <li>Evacuate to higher ground immediately</li>
                        <li>Follow emergency services instructions</li>
                        <li>Take essential items only</li>
                        <li>Do not return until authorities give clearance</li>
                    </ul>
                </div>
                
                <div style="background-color: #e7f3ff; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="color: #0c5460; margin-top: 0;">Threat Details:</h3>
                    <p><strong>Cyclone Probability:</strong> {cyclone_data.get('probability', 0)*100:.1f}%</p>
                    <p><strong>Storm Surge Level:</strong> {surge_data.get('threat_level', 'Unknown')}</p>
                    <p><strong>Estimated Water Level:</strong> {surge_data.get('total_water_level', 0):.2f}m</p>
                </div>
                
                <div style="background-color: #d4edda; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="color: #155724; margin-top: 0;">Emergency Contacts:</h3>
                    <p><strong>Emergency Services:</strong> 911</p>
                    <p><strong>Coastal Authority:</strong> [Your emergency number]</p>
                    <p><strong>Evacuation Hotline:</strong> [Your evacuation number]</p>
                </div>
                
                <p style="text-align: center; color: #666; font-size: 12px;">
                    This is an automated alert from the Coastal Threat Alert System (CTAS).
                    Please follow official instructions from emergency services.
                </p>
            </div>
        </body>
        </html>
        """
        
        sms_text = f"""🚨 EVACUATION ALERT 🚨
Threat Level: {threat_level}
Time: {datetime.now().strftime('%H:%M')}

⚠️ EVACUATE IMMEDIATELY
- Move to higher ground
- Follow emergency instructions
- Take essential items only

Emergency: 911
CTAS Alert System"""

        push_title = "🚨 Coastal Evacuation Alert"
        push_body = f"Threat Level: {threat_level} - Evacuate immediately to higher ground"
        
        return {
            "email_subject": email_subject,
            "email_body": email_body,
            "sms_text": sms_text,
            "push_title": push_title,
            "push_body": push_body
        }

    def _send_email_notification(self, email: str, message_data: Dict) -> bool:
        """
        Send email notification
        """
        try:
            if not all([self.smtp_username, self.smtp_password]):
                logger.warning("Email credentials not configured, skipping email notification")
                return False
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = message_data['email_subject']
            msg['From'] = self.smtp_username
            msg['To'] = email
            
            # Add HTML content
            html_part = MIMEText(message_data['email_body'], 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email notification sent to {email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email to {email}: {e}")
            return False

    def _send_sms_notification(self, phone: str, message: str) -> bool:
        """
        Send SMS notification
        """
        try:
            if not all([self.sms_api_key, self.sms_api_url]):
                logger.warning("SMS API not configured, skipping SMS notification")
                return False
            
            # Example using a generic SMS API
            # You can replace this with your preferred SMS service (Twilio, etc.)
            payload = {
                "api_key": self.sms_api_key,
                "to": phone,
                "message": message
            }
            
            response = requests.post(self.sms_api_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"SMS notification sent to {phone}")
                return True
            else:
                logger.error(f"SMS API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending SMS to {phone}: {e}")
            return False

    def _send_push_notification(self, device_token: str, message_data: Dict) -> bool:
        """
        Send push notification
        """
        try:
            if not all([self.push_api_key, self.push_api_url]):
                logger.warning("Push notification API not configured, skipping push notification")
                return False
            
            # Example using a generic push notification service
            # You can replace this with Firebase, OneSignal, etc.
            payload = {
                "api_key": self.push_api_key,
                "device_token": device_token,
                "title": message_data['push_title'],
                "body": message_data['push_body'],
                "priority": "high"
            }
            
            response = requests.post(self.push_api_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"Push notification sent to device {device_token[:10]}...")
                return True
            else:
                logger.error(f"Push API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending push notification: {e}")
            return False

    def _store_notification_record(self, threat_data: Dict, results: Dict) -> None:
        """
        Store notification record in database
        """
        try:
            if not self.supabase:
                logger.warning("Supabase not available, skipping notification record storage")
                return
            
            notification_record = {
                "timestamp": datetime.now().isoformat(),
                "threat_level": threat_data.get('overall_threat'),
                "threat_type": "evacuation",
                "total_users": results["total_users"],
                "email_sent": results["email_sent"],
                "sms_sent": results["sms_sent"],
                "push_sent": results["push_sent"],
                "failed": results["failed"],
                "threat_data": threat_data,
                "results": results
            }
            
            # Store in notifications table
            response = self.supabase.table('notifications').insert(notification_record).execute()
            
            if response.data:
                logger.info("Notification record stored in database")
            else:
                logger.warning("Failed to store notification record")
                
        except Exception as e:
            logger.error(f"Error storing notification record: {e}")

# Create a global instance
notification_service = NotificationService()
