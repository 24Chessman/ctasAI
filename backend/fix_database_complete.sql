-- Complete Database Schema Fix Script
-- Run this in your Supabase SQL editor to fix all missing columns

-- Add missing location column to profiles table
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS location TEXT;

-- Update existing records to have a default location
UPDATE profiles SET location = 'coastal_zone_1' WHERE location IS NULL;

-- Make location not null after setting default values
ALTER TABLE profiles ALTER COLUMN location SET NOT NULL;

-- Add any other missing columns that might be needed
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS phone TEXT;
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS role TEXT DEFAULT 'community';

-- Update existing records to have default role if missing
UPDATE profiles SET role = 'community' WHERE role IS NULL;

-- Make role not null after setting default values
ALTER TABLE profiles ALTER COLUMN role SET NOT NULL;

-- Add constraint for role values
ALTER TABLE profiles DROP CONSTRAINT IF EXISTS profiles_role_check;
ALTER TABLE profiles ADD CONSTRAINT profiles_role_check CHECK (role IN ('admin', 'authority', 'community'));

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_profiles_location ON profiles(location);
CREATE INDEX IF NOT EXISTS idx_profiles_role ON profiles(role);

-- Verify the complete table structure
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns 
WHERE table_name = 'profiles' 
ORDER BY ordinal_position;

-- Show sample data to verify
SELECT id, email, full_name, phone, location, role, created_at FROM profiles LIMIT 3;

-- Test if we can query by location
SELECT COUNT(*) as total_users, location, role 
FROM profiles 
GROUP BY location, role 
ORDER BY location, role;
