-- Supabase Database Setup Script
-- Run this in your Supabase SQL editor

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create profiles table for user information
CREATE TABLE IF NOT EXISTS profiles (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    phone TEXT,
    location TEXT,
    role TEXT DEFAULT 'community' CHECK (role IN ('admin', 'authority', 'community')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create notifications table for storing notification records
CREATE TABLE IF NOT EXISTS notifications (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    threat_level TEXT,
    threat_type TEXT DEFAULT 'evacuation',
    total_users INTEGER DEFAULT 0,
    email_sent INTEGER DEFAULT 0,
    sms_sent INTEGER DEFAULT 0,
    push_sent INTEGER DEFAULT 0,
    failed INTEGER DEFAULT 0,
    threat_data JSONB,
    results JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create user_sessions table for tracking user sessions
CREATE TABLE IF NOT EXISTS user_sessions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    session_token TEXT UNIQUE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create evacuation_zones table for location-based notifications
CREATE TABLE IF NOT EXISTS evacuation_zones (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    zone_name TEXT UNIQUE NOT NULL,
    zone_description TEXT,
    coordinates JSONB, -- Store as GeoJSON or similar
    threat_level TEXT DEFAULT 'low',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create user_zones table for mapping users to evacuation zones
CREATE TABLE IF NOT EXISTS user_zones (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    zone_id UUID REFERENCES evacuation_zones(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, zone_id)
);

-- Create RLS (Row Level Security) policies
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE evacuation_zones ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_zones ENABLE ROW LEVEL SECURITY;

-- Profiles policies
CREATE POLICY "Users can view their own profile" ON profiles
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile" ON profiles
    FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Admins can view all profiles" ON profiles
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'admin'
        )
    );

-- Notifications policies
CREATE POLICY "Admins can view all notifications" ON notifications
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'admin'
        )
    );

CREATE POLICY "Authorities can view notifications" ON notifications
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM profiles WHERE id = auth.uid() AND role IN ('admin', 'authority')
        )
    );

-- User sessions policies
CREATE POLICY "Users can view their own sessions" ON user_sessions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own sessions" ON user_sessions
    FOR DELETE USING (auth.uid() = user_id);

-- Evacuation zones policies
CREATE POLICY "Everyone can view evacuation zones" ON evacuation_zones
    FOR SELECT USING (true);

CREATE POLICY "Admins can manage evacuation zones" ON evacuation_zones
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'admin'
        )
    );

-- User zones policies
CREATE POLICY "Users can view their own zone assignments" ON user_zones
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Admins can manage all zone assignments" ON user_zones
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'admin'
        )
    );

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_profiles_email ON profiles(email);
CREATE INDEX IF NOT EXISTS idx_profiles_role ON profiles(role);
CREATE INDEX IF NOT EXISTS idx_notifications_timestamp ON notifications(timestamp);
CREATE INDEX IF NOT EXISTS idx_notifications_threat_level ON notifications(threat_level);
CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_sessions_expires_at ON user_sessions(expires_at);
CREATE INDEX IF NOT EXISTS idx_user_zones_user_id ON user_zones(user_id);
CREATE INDEX IF NOT EXISTS idx_user_zones_zone_id ON user_zones(zone_id);

-- Create functions for automatic timestamp updates
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for automatic timestamp updates
CREATE TRIGGER update_profiles_updated_at 
    BEFORE UPDATE ON profiles 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_evacuation_zones_updated_at 
    BEFORE UPDATE ON evacuation_zones 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample evacuation zones
INSERT INTO evacuation_zones (zone_name, zone_description, coordinates, threat_level) VALUES
('coastal_zone_1', 'Primary coastal evacuation zone', '{"lat": 25.7617, "lng": -80.1918}', 'low'),
('coastal_zone_2', 'Secondary coastal evacuation zone', '{"lat": 25.7907, "lng": -80.1300}', 'low'),
('high_risk_zone', 'High risk evacuation zone', '{"lat": 25.7749, "lng": -80.1977}', 'medium')
ON CONFLICT (zone_name) DO NOTHING;

-- Create a function to get users by location/zone
CREATE OR REPLACE FUNCTION get_users_by_zone(zone_name_param TEXT)
RETURNS TABLE (
    id UUID,
    email TEXT,
    full_name TEXT,
    phone TEXT,
    location TEXT,
    role TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.email, p.full_name, p.phone, p.location, p.role
    FROM profiles p
    JOIN user_zones uz ON p.id = uz.user_id
    JOIN evacuation_zones ez ON uz.zone_id = ez.id
    WHERE ez.zone_name = zone_name_param;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Grant necessary permissions
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO anon, authenticated;

-- Create a view for easy user management
CREATE OR REPLACE VIEW user_summary AS
SELECT 
    p.id,
    p.email,
    p.full_name,
    p.phone,
    p.location,
    p.role,
    p.created_at,
    COUNT(uz.zone_id) as assigned_zones,
    STRING_AGG(ez.zone_name, ', ') as zone_names
FROM profiles p
LEFT JOIN user_zones uz ON p.id = uz.user_id
LEFT JOIN evacuation_zones ez ON uz.zone_id = ez.id
GROUP BY p.id, p.email, p.full_name, p.phone, p.location, p.role, p.created_at;

-- Grant access to the view
GRANT SELECT ON user_summary TO anon, authenticated;
