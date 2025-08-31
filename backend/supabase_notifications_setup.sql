-- Supabase SQL script to set up notifications table
-- Run this in your Supabase SQL editor

-- Create notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    threat_level TEXT,
    threat_type TEXT DEFAULT 'evacuation',
    total_users INTEGER DEFAULT 0,
    email_sent INTEGER DEFAULT 0,
    sms_sent INTEGER DEFAULT 0,
    push_sent INTEGER DEFAULT 0,
    failed INTEGER DEFAULT 0,
    threat_data JSONB,
    results JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for better query performance
CREATE INDEX IF NOT EXISTS idx_notifications_timestamp ON notifications(timestamp);
CREATE INDEX IF NOT EXISTS idx_notifications_threat_level ON notifications(threat_level);
CREATE INDEX IF NOT EXISTS idx_notifications_threat_type ON notifications(threat_type);

-- Add RLS (Row Level Security) policies
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;

-- Policy to allow authenticated users to read notifications
CREATE POLICY "Allow authenticated users to read notifications" ON notifications
    FOR SELECT USING (auth.role() = 'authenticated');

-- Policy to allow service role to insert notifications
CREATE POLICY "Allow service role to insert notifications" ON notifications
    FOR INSERT WITH CHECK (auth.role() = 'service_role');

-- Add location field to profiles table if it doesn't exist
-- This is useful for location-based evacuation alerts
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'profiles' AND column_name = 'location') THEN
        ALTER TABLE profiles ADD COLUMN location TEXT;
    END IF;
END $$;

-- Add phone field to profiles table if it doesn't exist
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'profiles' AND column_name = 'phone') THEN
        ALTER TABLE profiles ADD COLUMN phone TEXT;
    END IF;
END $$;

-- Add device_token field to profiles table if it doesn't exist
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'profiles' AND column_name = 'device_token') THEN
        ALTER TABLE profiles ADD COLUMN device_token TEXT;
    END IF;
END $$;

-- Add notification preferences to profiles table
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'profiles' AND column_name = 'notification_preferences') THEN
        ALTER TABLE profiles ADD COLUMN notification_preferences JSONB DEFAULT '{"email": true, "sms": true, "push": true}'::jsonb;
    END IF;
END $$;

-- Create a view for notification statistics
CREATE OR REPLACE VIEW notification_stats AS
SELECT 
    DATE(timestamp) as date,
    threat_level,
    threat_type,
    COUNT(*) as total_notifications,
    SUM(total_users) as total_users_notified,
    SUM(email_sent) as total_emails_sent,
    SUM(sms_sent) as total_sms_sent,
    SUM(push_sent) as total_push_sent,
    SUM(failed) as total_failed
FROM notifications
GROUP BY DATE(timestamp), threat_level, threat_type
ORDER BY date DESC;

-- Grant permissions
GRANT SELECT ON notification_stats TO authenticated;
GRANT ALL ON notifications TO service_role;

-- Insert some sample data for testing (optional)
INSERT INTO notifications (
    threat_level, 
    threat_type, 
    total_users, 
    email_sent, 
    sms_sent, 
    push_sent, 
    failed,
    threat_data,
    results
) VALUES (
    'HIGH',
    'evacuation',
    150,
    120,
    80,
    45,
    5,
    '{"overall_threat": "HIGH", "cyclone": {"probability": 0.85}}'::jsonb,
    '{"email_sent": 120, "sms_sent": 80, "push_sent": 45, "failed": 5}'::jsonb
) ON CONFLICT DO NOTHING;

-- Create function to get notification statistics
CREATE OR REPLACE FUNCTION get_notification_stats(days_back INTEGER DEFAULT 7)
RETURNS TABLE (
    date DATE,
    threat_level TEXT,
    total_notifications BIGINT,
    total_users_notified BIGINT,
    success_rate NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ns.date,
        ns.threat_level,
        ns.total_notifications,
        ns.total_users_notified,
        CASE 
            WHEN (ns.total_emails_sent + ns.total_sms_sent + ns.total_push_sent) > 0 
            THEN ROUND(
                ((ns.total_emails_sent + ns.total_sms_sent + ns.total_push_sent)::NUMERIC / 
                (ns.total_emails_sent + ns.total_sms_sent + ns.total_push_sent + ns.total_failed)) * 100, 2
            )
            ELSE 0 
        END as success_rate
    FROM notification_stats ns
    WHERE ns.date >= CURRENT_DATE - days_back
    ORDER BY ns.date DESC, ns.threat_level;
END;
$$ LANGUAGE plpgsql;

-- Grant execute permission on the function
GRANT EXECUTE ON FUNCTION get_notification_stats(INTEGER) TO authenticated;
