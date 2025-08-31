import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'https://placeholder.supabase.co'
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || 'placeholder-key'

// Only throw error in production
if (import.meta.env.PROD && (!import.meta.env.VITE_SUPABASE_URL || !import.meta.env.VITE_SUPABASE_ANON_KEY)) {
  throw new Error('Missing Supabase environment variables')
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Database types
export interface User {
  id: string
  email: string
  full_name: string
  role: 'admin' | 'authority' | 'community'
  created_at: string
  updated_at: string
}

export interface UserProfile {
  id: string
  full_name: string
  gender: string
  age: number
  address: string
  city: string
  state: string
  zip_code: string
  country: string
  location_url?: string
  plus_code?: string
  role: 'admin' | 'authority' | 'community'
  id_file_url?: string
  created_at: string
  updated_at: string
}
