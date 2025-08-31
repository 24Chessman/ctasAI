# Supabase Setup Guide

## 1. Environment Variables

Create a `.env` file in the frontend directory with the following variables:

```env
VITE_SUPABASE_URL=your_supabase_project_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

## 2. Database Schema

Run the following SQL in your Supabase SQL editor to create the required tables:

```sql
-- Create user_profiles table
CREATE TABLE user_profiles (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name TEXT NOT NULL,
  gender TEXT NOT NULL,
  age INTEGER NOT NULL,
  address TEXT NOT NULL,
  city TEXT NOT NULL,
  state TEXT NOT NULL,
  zip_code TEXT NOT NULL,
  country TEXT NOT NULL DEFAULT 'India',
  location_url TEXT,
  plus_code TEXT,
  role TEXT NOT NULL CHECK (role IN ('admin', 'authority', 'community')),
  id_file_url TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view their own profile" ON user_profiles
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can update their own profile" ON user_profiles
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own profile" ON user_profiles
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Create function to handle user creation
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO user_profiles (user_id, full_name, role)
  VALUES (NEW.id, NEW.raw_user_meta_data->>'full_name', NEW.raw_user_meta_data->>'role');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger for new user creation
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_user();
```

## 3. Authentication Settings

In your Supabase dashboard:

1. Go to Authentication > Settings
2. Enable "Enable email confirmations"
3. Set your site URL
4. Configure email templates if needed

## 4. Storage Setup (for ID files)

Create a storage bucket for ID files:

```sql
-- Create storage bucket for ID files
INSERT INTO storage.buckets (id, name, public) VALUES ('id-files', 'id-files', false);

-- Create policy for ID file uploads
CREATE POLICY "Users can upload their own ID files" ON storage.objects
  FOR INSERT WITH CHECK (bucket_id = 'id-files' AND auth.uid()::text = (storage.foldername(name))[1]);

-- Create policy for ID file access
CREATE POLICY "Users can view their own ID files" ON storage.objects
  FOR SELECT USING (bucket_id = 'id-files' AND auth.uid()::text = (storage.foldername(name))[1]);
```

## 5. Testing

1. Start the development server: `npm run dev`
2. Try registering a new user
3. Check your email for verification
4. Try logging in with the registered user
