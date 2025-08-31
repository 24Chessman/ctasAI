# 🚨 Coastal Threat Alert System - Evacuation Notification System

## Overview

The evacuation notification system automatically sends evacuation alerts to registered users when high-level threats are detected. The system supports multiple notification channels including email, SMS, and push notifications.

## Features

### 🔔 Automatic Threat Detection
- Monitors weather data and runs threat detection algorithms
- Automatically triggers evacuation alerts when threat level is HIGH or EXTREME
- Integrates with existing cyclone and storm surge prediction systems

### 📧 Multi-Channel Notifications
- **Email Notifications**: Rich HTML emails with detailed evacuation instructions
- **SMS Notifications**: Concise text messages for immediate alerts
- **Push Notifications**: Mobile app notifications (configurable)

### 🎯 Location-Based Targeting
- Send alerts to users in specific locations/zones
- Filter users by geographic areas for targeted evacuations
- Support for custom location-based alerting

### 📊 Comprehensive Tracking
- Track notification delivery success rates
- Store notification history in database
- Monitor system performance and user engagement

## System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Threat        │    │   Alert          │    │   Notification  │
│   Detection     │───▶│   System         │───▶│   Service       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │   Database       │    │   Email/SMS/    │
                       │   (Supabase)     │    │   Push APIs     │
                       └──────────────────┘    └─────────────────┘
```

## Setup Instructions

### 1. Database Setup

Run the SQL script in your Supabase SQL editor:

```sql
-- Run the contents of supabase_notifications_setup.sql
```

This will create:
- `notifications` table for storing alert records
- Additional fields in `profiles` table (location, phone, device_token)
- Notification statistics views and functions

### 2. Environment Variables

Add these to your `backend/.env` file:

```env
# Supabase Configuration (already configured)
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key

# Email Configuration (for Gmail)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# SMS Configuration (for Twilio or similar)
SMS_API_KEY=your_sms_api_key
SMS_API_URL=https://api.twilio.com/2010-04-01/Accounts/your_account/Messages.json

# Push Notification Configuration (for Firebase or similar)
PUSH_API_KEY=your_push_api_key
PUSH_API_URL=https://fcm.googleapis.com/fcm/send
```

### 3. Email Setup (Gmail Example)

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
3. Use the generated password as `SMTP_PASSWORD`

### 4. SMS Setup (Twilio Example)

1. Sign up for a Twilio account
2. Get your Account SID and Auth Token
3. Configure the SMS API URL with your Twilio credentials

## API Endpoints

### Evacuation Management

#### Test Evacuation System
```http
POST /api/v1/evacuation/test-evacuation
```
Runs real threat detection and sends alerts if threats are found.

#### Trigger Evacuation Alert
```http
POST /api/v1/evacuation/trigger-evacuation
Content-Type: application/json

{
  "location": "Mumbai, Zone A",
  "threat_level": "HIGH",
  "custom_message": "Custom evacuation message"
}
```

#### Send Custom Alert
```http
POST /api/v1/evacuation/send-custom-alert
Content-Type: application/json

{
  "message": "Custom alert message",
  "title": "Custom Alert",
  "target_location": "Mumbai"
}
```

#### Get Registered Users
```http
GET /api/v1/evacuation/users
```

#### Get Users by Location
```http
GET /api/v1/evacuation/users/location/{location}
```

## Usage Examples

### Testing the System

1. **Start the backend server:**
   ```bash
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Test evacuation alerts:**
   - Use the frontend test panel (admin dashboard)
   - Or use curl commands:
   ```bash
   # Test real threat detection
   curl -X POST http://localhost:8000/api/v1/evacuation/test-evacuation
   
   # Trigger evacuation alert
   curl -X POST http://localhost:8000/api/v1/evacuation/trigger-evacuation \
     -H "Content-Type: application/json" \
     -d '{"location": "Mumbai", "threat_level": "HIGH"}'
   ```

### Frontend Testing

1. Log in as an admin user
2. Navigate to the Dashboard
3. Use the "Evacuation Alert Testing Panel" to:
   - Test real threat detection
   - Trigger evacuation alerts
   - Send custom messages
   - View registered users

## Notification Message Templates

### Email Template
- Rich HTML formatting with emergency styling
- Threat level indicators
- Detailed evacuation instructions
- Emergency contact information
- Professional branding

### SMS Template
```
🚨 EVACUATION ALERT 🚨
Threat Level: HIGH
Time: 14:30

⚠️ EVACUATE IMMEDIATELY
- Move to higher ground
- Follow emergency instructions
- Take essential items only

Emergency: 911
CTAS Alert System
```

### Push Notification
- Title: "🚨 Coastal Evacuation Alert"
- Body: "Threat Level: HIGH - Evacuate immediately to higher ground"

## Database Schema

### Notifications Table
```sql
CREATE TABLE notifications (
    id UUID PRIMARY KEY,
    timestamp TIMESTAMPTZ,
    threat_level TEXT,
    threat_type TEXT,
    total_users INTEGER,
    email_sent INTEGER,
    sms_sent INTEGER,
    push_sent INTEGER,
    failed INTEGER,
    threat_data JSONB,
    results JSONB
);
```

### Enhanced Profiles Table
```sql
ALTER TABLE profiles ADD COLUMN location TEXT;
ALTER TABLE profiles ADD COLUMN phone TEXT;
ALTER TABLE profiles ADD COLUMN device_token TEXT;
ALTER TABLE profiles ADD COLUMN notification_preferences JSONB;
```

## Monitoring and Analytics

### Notification Statistics
- Track delivery success rates
- Monitor user engagement
- Analyze notification patterns
- Generate reports

### Database Views
```sql
-- Get notification statistics
SELECT * FROM notification_stats;

-- Get notification success rates
SELECT * FROM get_notification_stats(7); -- Last 7 days
```

## Security Considerations

### Row Level Security (RLS)
- Notifications table has RLS enabled
- Only authenticated users can read notifications
- Service role can insert notifications

### Data Privacy
- User phone numbers are masked in API responses
- Email addresses are partially hidden
- Sensitive data is not logged

## Troubleshooting

### Common Issues

1. **Email not sending:**
   - Check SMTP credentials
   - Verify Gmail App Password
   - Check firewall settings

2. **SMS not sending:**
   - Verify SMS API credentials
   - Check phone number format
   - Ensure SMS service is active

3. **No users found:**
   - Verify Supabase connection
   - Check profiles table exists
   - Ensure users are registered

4. **Backend connection errors:**
   - Check if backend server is running
   - Verify CORS settings
   - Check network connectivity

### Debug Mode

Enable debug logging by setting:
```env
LOG_LEVEL=DEBUG
```

## Future Enhancements

### Planned Features
- [ ] Webhook notifications
- [ ] Voice call alerts
- [ ] Social media integration
- [ ] Advanced targeting algorithms
- [ ] Notification scheduling
- [ ] A/B testing for message effectiveness

### Integration Possibilities
- [ ] Emergency services APIs
- [ ] Weather service integrations
- [ ] Geographic information systems
- [ ] Mobile app push notifications
- [ ] IoT device alerts

## Support

For technical support or questions about the evacuation notification system:

1. Check the logs in the backend console
2. Verify all environment variables are set
3. Test individual components using the API endpoints
4. Review the database schema and permissions

## License

This evacuation notification system is part of the Coastal Threat Alert System (CTAS) developed for HackOut'25.
