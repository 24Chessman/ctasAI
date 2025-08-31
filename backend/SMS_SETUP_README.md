# SMS Alert System Setup Guide

## Overview

The Coastal Threat Alert System (CTAS) now includes comprehensive SMS alert functionality that allows you to send emergency notifications to users based on their phone numbers. This system supports multiple SMS providers and provides both automated and manual alert capabilities.

## Features

- **High Alert SMS**: Send emergency alerts to all users with phone numbers
- **Bulk SMS**: Send custom messages to specific phone numbers
- **Test SMS**: Verify SMS configuration before sending alerts
- **Multiple Providers**: Support for Twilio, Nexmo (Vonage), AWS SNS, and custom APIs
- **Phone Validation**: Automatic phone number validation and formatting
- **Location-based Alerts**: Send alerts to users in specific locations
- **Delivery Tracking**: Monitor SMS delivery success and failure rates
- **Database Integration**: Store notification records and user phone numbers

## Database Setup

### 1. Update Profiles Table

Run the following SQL in your Supabase SQL editor to add phone number support:

```sql
-- Add phone column to profiles table if it doesn't exist
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS phone TEXT;

-- Add location column if it doesn't exist
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS location TEXT;

-- Add notification preferences
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS notification_preferences JSONB 
DEFAULT '{"email": true, "sms": true, "push": true}'::jsonb;

-- Create index for better performance
CREATE INDEX IF NOT EXISTS idx_profiles_phone ON profiles(phone);
CREATE INDEX IF NOT EXISTS idx_profiles_location ON profiles(location);
```

### 2. Create Notifications Table

```sql
-- Create notifications table for tracking SMS alerts
CREATE TABLE IF NOT EXISTS notifications (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    threat_level TEXT,
    threat_type TEXT DEFAULT 'sms_alert',
    total_users INTEGER DEFAULT 0,
    sms_sent INTEGER DEFAULT 0,
    failed INTEGER DEFAULT 0,
    threat_data JSONB,
    results JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_notifications_timestamp ON notifications(timestamp);
CREATE INDEX IF NOT EXISTS idx_notifications_threat_level ON notifications(threat_level);
```

## SMS Provider Configuration

### Option 1: Twilio (Recommended)

1. **Sign up for Twilio**: Create an account at [twilio.com](https://twilio.com)
2. **Get your credentials**:
   - Account SID
   - Auth Token
   - Twilio Phone Number

3. **Add to your `.env` file**:
```env
# Twilio Configuration
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=your_twilio_phone_number
```

### Option 2: Nexmo (Vonage)

1. **Sign up for Nexmo**: Create an account at [nexmo.com](https://nexmo.com)
2. **Get your credentials**:
   - API Key
   - API Secret
   - Nexmo Phone Number

3. **Add to your `.env` file**:
```env
# Nexmo Configuration
NEXMO_API_KEY=your_api_key_here
NEXMO_API_SECRET=your_api_secret_here
NEXMO_PHONE_NUMBER=your_nexmo_phone_number
```

### Option 3: AWS SNS

1. **Set up AWS SNS**: Configure AWS SNS in your AWS console
2. **Get your credentials**:
   - AWS Access Key ID
   - AWS Secret Access Key
   - AWS Region

3. **Add to your `.env` file**:
```env
# AWS SNS Configuration
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=us-east-1
```

### Option 4: Custom SMS API

1. **Configure your custom SMS provider**:
```env
# Custom SMS Configuration
SMS_API_KEY=your_api_key_here
SMS_API_URL=https://your-sms-provider.com/api/send
```

## Backend Setup

### 1. Install Dependencies

The SMS service uses the following Python packages (already included in requirements.txt):
- `requests` - For HTTP API calls
- `re` - For phone number validation

### 2. Environment Variables

Add the following to your `backend/.env` file:

```env
# SMS Configuration
SMS_API_KEY=your_api_key_here
SMS_API_URL=your_api_url_here

# Twilio (if using Twilio)
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=your_twilio_phone_number

# Nexmo (if using Nexmo)
NEXMO_API_KEY=your_api_key_here
NEXMO_API_SECRET=your_api_secret_here
NEXMO_PHONE_NUMBER=your_nexmo_phone_number

# AWS SNS (if using AWS)
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=us-east-1
```

### 3. Start the Backend Server

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### 1. SMS Status
```
GET /api/v1/sms/sms-status
```
Returns SMS service configuration status.

### 2. Test SMS
```
POST /api/v1/sms/test-sms
```
Send a test SMS to verify configuration.

**Request Body:**
```json
{
  "phone": "+919876543210",
  "message": "Test SMS from CTAS Alert System"
}
```

### 3. Send High Alert
```
POST /api/v1/sms/send-high-alert
```
Send emergency alerts to all users with phone numbers.

**Request Body:**
```json
{
  "threat_level": "HIGH",
  "threat_data": {
    "cyclone": {
      "probability": 0.85,
      "intensity": "Category 3"
    },
    "storm_surge": {
      "threat_level": "HIGH",
      "total_water_level": 3.2
    }
  },
  "location": "coastal_zone_1",
  "message": "Custom alert message"
}
```

### 4. Send Bulk SMS
```
POST /api/v1/sms/send-bulk-sms
```
Send SMS to specific phone numbers.

**Request Body:**
```json
{
  "phone_numbers": ["+919876543210", "+919876543211"],
  "message": "Your custom message here"
}
```

### 5. Get Users with Phone Numbers
```
GET /api/v1/sms/users-with-phones?location=coastal_zone_1
```
Get all users with valid phone numbers.

## Frontend Usage

### 1. Access SMS Alerts Page

Navigate to `/sms-alerts` in your application to access the SMS management interface.

### 2. Features Available

- **SMS Status**: View current SMS configuration and user count
- **Test SMS**: Send test messages to verify setup
- **High Alert SMS**: Send emergency alerts to all users
- **Bulk SMS**: Send custom messages to specific numbers
- **Results Tracking**: Monitor delivery success and failures

### 3. Testing the System

1. **Configure SMS Provider**: Set up your chosen SMS provider
2. **Test Configuration**: Use the Test SMS feature
3. **Add User Phone Numbers**: Ensure users have phone numbers in the database
4. **Send Test Alert**: Try sending a high alert to verify functionality

## Phone Number Format

The system supports various phone number formats:

- **Indian Numbers**: `9876543210`, `+919876543210`, `919876543210`
- **International**: `+1234567890`, `1234567890`
- **Formatted**: `+91 98765 43210`, `(987) 654-3210`

The system automatically:
- Validates phone number format
- Adds country code if missing (defaults to +91 for India)
- Removes formatting characters
- Ensures proper length (7-15 digits)

## Message Templates

### High Alert Template
```
🚨 COASTAL THREAT ALERT 🚨
Level: HIGH
Time: 14:30

⚠️ IMMEDIATE ACTION REQUIRED
- Evacuate to higher ground
- Follow emergency instructions
- Take essential items only

Emergency: 911
CTAS Alert System

Cyclone Probability: 85.0%
Storm Surge: HIGH
```

### Custom Message Support
You can override the default template by providing a custom message in the API request.

## Error Handling

The system includes comprehensive error handling:

- **Invalid Phone Numbers**: Automatically filtered out
- **API Failures**: Logged and reported
- **Rate Limiting**: Handled gracefully
- **Network Issues**: Retry mechanisms
- **Configuration Errors**: Clear error messages

## Monitoring and Analytics

### Database Queries

```sql
-- Get SMS notification statistics
SELECT 
    DATE(timestamp) as date,
    threat_level,
    COUNT(*) as total_alerts,
    SUM(sms_sent) as total_sms_sent,
    SUM(failed) as total_failed,
    AVG(sms_sent::float / total_users) * 100 as success_rate
FROM notifications 
WHERE threat_type = 'sms_alert'
GROUP BY DATE(timestamp), threat_level
ORDER BY date DESC;

-- Get users with phone numbers by location
SELECT 
    location,
    COUNT(*) as users_with_phones
FROM profiles 
WHERE phone IS NOT NULL AND phone != ''
GROUP BY location;
```

### Log Monitoring

Check the backend logs for SMS-related events:
```bash
# Monitor SMS logs
tail -f backend/logs/app.log | grep -i sms
```

## Security Considerations

1. **API Key Protection**: Store API keys securely in environment variables
2. **Rate Limiting**: Implement rate limiting to prevent abuse
3. **Phone Number Privacy**: Mask phone numbers in logs and responses
4. **Access Control**: Restrict SMS functionality to authorized users
5. **Audit Trail**: All SMS activities are logged and stored

## Troubleshooting

### Common Issues

1. **SMS Not Sending**
   - Check API credentials
   - Verify phone number format
   - Check SMS provider status
   - Review error logs

2. **Invalid Phone Numbers**
   - Ensure proper country code
   - Check for formatting issues
   - Verify number length

3. **API Configuration Errors**
   - Verify environment variables
   - Check API endpoint URLs
   - Ensure proper authentication

4. **No Users Found**
   - Check database connection
   - Verify user phone numbers exist
   - Check location filters

### Debug Commands

```bash
# Test SMS configuration
curl -X POST http://localhost:8000/api/v1/sms/test-sms \
  -H "Content-Type: application/json" \
  -d '{"phone": "+919876543210", "message": "Test"}'

# Check SMS status
curl http://localhost:8000/api/v1/sms/sms-status

# Get users with phones
curl http://localhost:8000/api/v1/sms/users-with-phones
```

## Best Practices

1. **Test Before Production**: Always test SMS functionality in development
2. **Monitor Costs**: SMS services charge per message
3. **Rate Limiting**: Implement appropriate rate limits
4. **Error Handling**: Handle failures gracefully
5. **User Consent**: Ensure users have opted in for SMS alerts
6. **Message Length**: Keep messages concise (SMS character limits)
7. **Emergency Protocols**: Have backup communication methods

## Support

For issues or questions:
1. Check the logs for error messages
2. Verify configuration settings
3. Test with the provided endpoints
4. Review this documentation

## Future Enhancements

- **SMS Templates**: Pre-defined message templates
- **Scheduled Alerts**: Time-based alert scheduling
- **Delivery Reports**: Detailed delivery status tracking
- **Multi-language Support**: Support for multiple languages
- **Advanced Filtering**: More granular user targeting
- **Webhook Integration**: Real-time delivery notifications
