# 🗄️ Database Setup Guide for CTAS AI

## 📋 Prerequisites

- Supabase account with the following credentials:
  - **URL**: `https://bdxchhewjbfzydeyjces.supabase.co`
  - **Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJkeGNoaGV3amJmenlkZXlqY2VzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTY1MDA1NTUsImV4cCI6MjA3MjA3NjU1NX0.t58O9RpsmRPv7_5jJFSxJkzHX2hIt0jsgrFXUHGOSb0`

## 🚀 Step 1: Set Up Supabase Database

### 1.1 Access Supabase Dashboard
1. Go to [https://supabase.com](https://supabase.com)
2. Sign in to your account
3. Navigate to your project: `bdxchhewjbfzydeyjces`

### 1.2 Run Database Setup Script
1. In the Supabase dashboard, go to **SQL Editor**
2. Copy the contents of `supabase_setup.sql`
3. Paste and run the script
4. Verify all tables are created successfully

### 1.3 Verify Table Creation
Check that these tables exist:
- ✅ `profiles` - User profiles and authentication
- ✅ `notifications` - Notification records
- ✅ `user_sessions` - User session management
- ✅ `evacuation_zones` - Geographic zones for alerts
- ✅ `user_zones` - User-zone assignments

## 🔧 Step 2: Configure Backend Environment

### 2.1 Create Environment File
Create `backend/.env` with:

```bash
# Supabase Configuration
SUPABASE_URL=https://bdxchhewjbfzydeyjces.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJkeGNoaGV3amJmenlkZXlqY2VzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTY1MDA1NTUsImV4cCI6MjA3MjA3NjU1NX0.t58O9RpsmRPv7_5jJFSxJkzHX2hIt0jsgrFXUHGOSb0

# Email Configuration (Optional - for sending notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# SMS Configuration (Optional)
SMS_API_KEY=your-sms-api-key
SMS_API_URL=your-sms-api-url

# Push Notification Configuration (Optional)
PUSH_API_KEY=your-push-api-key
PUSH_API_URL=your-push-api-url
```

### 2.2 Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

## 🧪 Step 3: Test the Setup

### 3.1 Start Backend Server
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3.2 Run Comprehensive Tests
```bash
cd backend
python test_database_setup.py
```

### 3.3 Test Web Dashboard
1. Open `backend/test_notifications.html` in your browser
2. Test notification features
3. Verify user management

## 📱 Step 4: Test Authentication

### 4.1 Test User Registration
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123",
    "full_name": "Test User",
    "phone": "+1234567890",
    "location": "coastal_zone_1"
  }'
```

### 4.2 Test User Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

## 🔔 Step 5: Test Notifications

### 5.1 Test Notification Service
```bash
curl -X POST http://localhost:8000/api/v1/alerts/test-notification \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "threat_level": "HIGH",
    "cyclone_probability": 0.8,
    "storm_surge_level": "high",
    "water_level": 3.0,
    "test_email": "your-email@example.com"
  }'
```

### 5.2 Test Alert System
```bash
curl -X POST http://localhost:8000/api/v1/alerts/test-alert-system \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📊 Step 6: Verify Database Records

### 6.1 Check Supabase Dashboard
1. Go to **Table Editor** in Supabase
2. Verify data in:
   - `profiles` table
   - `notifications` table
   - `user_sessions` table

### 6.2 Check API Responses
```bash
# Get all users
curl http://localhost:8000/api/v1/alerts/users

# Get user profile
curl http://localhost:8000/api/v1/auth/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🚨 Troubleshooting

### Common Issues

#### 1. "Supabase configuration not found"
- Check your `.env` file exists
- Verify `SUPABASE_URL` and `SUPABASE_KEY` are set correctly

#### 2. "Database connection failed"
- Ensure Supabase project is active
- Check if the setup script ran successfully
- Verify RLS policies are in place

#### 3. "Authentication failed"
- Check if user exists in `profiles` table
- Verify Supabase auth is enabled
- Check RLS policies for authentication

#### 4. "Notification service not working"
- Verify email/SMS credentials if configured
- Check notification records in database
- Review logs for specific error messages

### Debug Commands

```bash
# Check backend logs
tail -f backend/logs/app.log

# Test database connection directly
python -c "from app.services.notification_service import notification_service; print(notification_service.get_all_users())"

# Check environment variables
python -c "from app.core.config import settings; print(f'SUPABASE_URL: {settings.SUPABASE_URL}')"
```

## ✅ Success Criteria

Your setup is complete when:

1. ✅ Backend server starts without errors
2. ✅ Database connection test passes
3. ✅ User registration and login work
4. ✅ Notification service can send alerts
5. ✅ All API endpoints respond correctly
6. ✅ Database tables contain expected data

## 🔗 Next Steps

After successful setup:

1. **Frontend Integration**: Connect your React/Vue frontend to the new API
2. **Email Configuration**: Set up SMTP for real notification delivery
3. **SMS Integration**: Add Twilio or similar service for SMS alerts
4. **Push Notifications**: Integrate Firebase or OneSignal
5. **Production Deployment**: Deploy to your production environment

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review backend logs for error details
3. Verify Supabase project status
4. Check API endpoint responses
5. Test individual components step by step

---

**Happy coding! 🚀**
