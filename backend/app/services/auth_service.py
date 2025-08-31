# backend/app/services/auth_service.py
import logging
import jwt
import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from supabase import create_client, Client
from app.core.config import settings
from app.core.ssl_utils import configure_ssl, create_supabase_client_options
from app.core.utils import clean_profile_data, serialize_datetime

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self):
        """Initialize authentication service"""
        # Configure SSL settings first
        configure_ssl()
        
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
                logger.info("Auth service: Supabase client initialized successfully")
            except Exception as e:
                logger.error(f"Auth service: Failed to initialize Supabase client: {e}")
                # Try fallback without SSL verification
                try:
                    logger.info("Auth service: Attempting fallback connection without SSL verification")
                    self.supabase: Client = create_client(
                        self.supabase_url, 
                        self.supabase_key
                    )
                    logger.info("Auth service: Fallback connection successful")
                except Exception as fallback_e:
                    logger.error(f"Auth service: Fallback connection also failed: {fallback_e}")
                    self.supabase = None
        else:
            logger.error("Auth service: Supabase configuration not found")
            self.supabase = None

    def register_user(self, email: str, password: str, full_name: str, phone: str = None, location: str = None) -> Dict:
        """
        Register a new user
        """
        try:
            if not self.supabase:
                return {"success": False, "message": "Database not available"}
            
            # Check if user already exists
            existing_user = self.supabase.table('profiles').select('*').eq('email', email).execute()
            if existing_user.data:
                return {"success": False, "message": "User with this email already exists"}
            
            # Create user in Supabase auth
            auth_response = self.supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            if auth_response.user:
                user_id = auth_response.user.id
                
                # Create profile record
                profile_data = {
                    "id": user_id,
                    "email": email,
                    "full_name": full_name,
                    "phone": phone,
                    "location": location,
                    "role": "community"
                }
                
                profile_response = self.supabase.table('profiles').insert(profile_data).execute()
                
                if profile_response.data:
                    logger.info(f"User registered successfully: {email}")
                    return {
                        "success": True,
                        "message": "User registered successfully",
                        "user_id": user_id,
                        "email": email
                    }
                else:
                    # Clean up auth user if profile creation fails
                    logger.error("Profile creation failed, cleaning up auth user")
                    return {"success": False, "message": "Failed to create user profile"}
            else:
                return {"success": False, "message": "Failed to create user account"}
                
        except Exception as e:
            logger.error(f"Error registering user: {e}")
            return {"success": False, "message": str(e)}

    def login_user(self, email: str, password: str) -> Dict:
        """
        Login user and return session token
        """
        try:
            if not self.supabase:
                return {"success": False, "message": "Database not available"}
            
            # Authenticate user
            auth_response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if auth_response.user and auth_response.session:
                user_id = auth_response.user.id
                access_token = auth_response.session.access_token
                refresh_token = auth_response.session.refresh_token
                
                # Get user profile
                profile_response = self.supabase.table('profiles').select('*').eq('id', user_id).execute()
                profile = profile_response.data[0] if profile_response.data else None
                
                # Create session record
                session_data = {
                    "user_id": user_id,
                    "session_token": access_token,
                    "expires_at": datetime.now() + timedelta(hours=24)
                }
                
                self.supabase.table('user_sessions').insert(session_data).execute()
                
                logger.info(f"User logged in successfully: {email}")
                
                # Clean profile data to avoid datetime serialization issues
                cleaned_profile = clean_profile_data(profile) if profile else {}
                
                return {
                    "success": True,
                    "message": "Login successful",
                    "user": {
                        "id": user_id,
                        "email": email,
                        "full_name": cleaned_profile.get('full_name'),
                        "role": cleaned_profile.get('role', 'community'),
                        "phone": cleaned_profile.get('phone'),
                        "location": cleaned_profile.get('location')
                    },
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            else:
                return {"success": False, "message": "Invalid credentials"}
                
        except Exception as e:
            logger.error(f"Error logging in user: {e}")
            return {"success": False, "message": str(e)}

    def logout_user(self, user_id: str, session_token: str) -> Dict:
        """
        Logout user and invalidate session
        """
        try:
            if not self.supabase:
                return {"success": False, "message": "Database not available"}
            
            # Remove session record
            self.supabase.table('user_sessions').delete().eq('user_id', user_id).eq('session_token', session_token).execute()
            
            # Sign out from Supabase
            self.supabase.auth.sign_out()
            
            logger.info(f"User logged out successfully: {user_id}")
            return {"success": True, "message": "Logout successful"}
            
        except Exception as e:
            logger.error(f"Error logging out user: {e}")
            return {"success": False, "message": str(e)}

    def verify_token(self, token: str) -> Optional[Dict]:
        """
        Verify JWT token and return user info
        """
        try:
            if not self.supabase:
                return None
            
            # Verify token with Supabase
            user = self.supabase.auth.get_user(token)
            
            if user:
                return {
                    "id": user.id,
                    "email": user.email,
                    "role": "community"  # Default role, can be enhanced
                }
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error verifying token: {e}")
            return None

    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """
        Get user profile by ID
        """
        try:
            if not self.supabase:
                return None
            
            response = self.supabase.table('profiles').select('*').eq('id', user_id).execute()
            
            if response.data:
                # Clean profile data to avoid datetime serialization issues
                return clean_profile_data(response.data[0])
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error getting user profile: {e}")
            return None

    def update_user_profile(self, user_id: str, profile_data: Dict) -> Dict:
        """
        Update user profile
        """
        try:
            if not self.supabase:
                return {"success": False, "message": "Database not available"}
            
            # Remove id from profile_data to avoid conflicts
            if 'id' in profile_data:
                del profile_data['id']
            
            response = self.supabase.table('profiles').update(profile_data).eq('id', user_id).execute()
            
            if response.data:
                logger.info(f"User profile updated successfully: {user_id}")
                return {"success": True, "message": "Profile updated successfully"}
            else:
                return {"success": False, "message": "Failed to update profile"}
                
        except Exception as e:
            logger.error(f"Error updating user profile: {e}")
            return {"success": False, "message": str(e)}

    def change_user_password(self, user_id: str, current_password: str, new_password: str) -> Dict:
        """
        Change user password
        """
        try:
            if not self.supabase:
                return {"success": False, "message": "Database not available"}
            
            # Get user email first
            profile = self.get_user_profile(user_id)
            if not profile:
                return {"success": False, "message": "User not found"}
            
            # Update password in Supabase auth
            auth_response = self.supabase.auth.update_user({
                "password": new_password
            })
            
            if auth_response.user:
                logger.info(f"User password changed successfully: {user_id}")
                return {"success": True, "message": "Password changed successfully"}
            else:
                return {"success": False, "message": "Failed to change password"}
                
        except Exception as e:
            logger.error(f"Error changing user password: {e}")
            return {"success": False, "message": str(e)}

    def delete_user(self, user_id: str) -> Dict:
        """
        Delete user account
        """
        try:
            if not self.supabase:
                return {"success": False, "message": "Database not available"}
            
            # Delete profile record
            self.supabase.table('profiles').delete().eq('id', user_id).execute()
            
            # Delete user sessions
            self.supabase.table('user_sessions').delete().eq('user_id', user_id).execute()
            
            # Note: User deletion from Supabase auth requires admin privileges
            # This is handled at the database level with CASCADE
            
            logger.info(f"User deleted successfully: {user_id}")
            return {"success": True, "message": "User deleted successfully"}
            
        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            return {"success": False, "message": str(e)}

# Create a global instance
auth_service = AuthService()
