-- Fix Database Schema Script
-- Run this in your Supabase SQL editor to fix the profiles table

-- Add missing email column to profiles table
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS email TEXT;

-- Make email unique and not null (after adding it)
UPDATE profiles SET email = 'user_' || id::text || '@example.com' WHERE email IS NULL;
ALTER TABLE profiles ALTER COLUMN email SET NOT NULL;
ALTER TABLE profiles ADD CONSTRAINT profiles_email_unique UNIQUE (email);

-- Update existing records to have unique emails
UPDATE profiles 
SET email = 'user_' || id::text || '@example.com' 
WHERE email = 'user_' || id::text || '@example.com' 
AND id IN (
    SELECT id FROM profiles 
    GROUP BY id 
    HAVING COUNT(*) > 1
);

-- Create index on email column for better performance
CREATE INDEX IF NOT EXISTS idx_profiles_email ON profiles(email);

-- Verify the table structure
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns 
WHERE table_name = 'profiles' 
ORDER BY ordinal_position;

-- Show sample data
SELECT * FROM profiles LIMIT 3;
