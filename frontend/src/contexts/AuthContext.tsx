import React, { createContext, useContext, useEffect, useState } from 'react'
import { apiService, UserProfile, AuthResponse } from '@/services/api'

interface AuthContextType {
  user: UserProfile | null
  session: { access_token: string; refresh_token: string } | null
  loading: boolean
  signUp: (email: string, password: string, userData: any) => Promise<{ error: any }>
  signIn: (email: string, password: string) => Promise<{ error: any }>
  signOut: () => Promise<void>
  resetPassword: (email: string) => Promise<{ error: any }>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

interface AuthProviderProps {
  children: React.ReactNode
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<UserProfile | null>(null)
  const [session, setSession] = useState<{ access_token: string; refresh_token: string } | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if user is already logged in (check localStorage for token)
    const checkAuthStatus = async () => {
      try {
        const token = localStorage.getItem('access_token')
        if (token) {
          // Verify token with backend
          const response = await apiService.verifyToken(token)
          if (response.success && response.data) {
            setUser(response.data)
            setSession({
              access_token: token,
              refresh_token: localStorage.getItem('refresh_token') || ''
            })
          } else {
            // Token is invalid, clear storage
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
          }
        }
      } catch (error) {
        console.error('Error checking auth status:', error)
        // Clear invalid tokens
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
      } finally {
        setLoading(false)
      }
    }

    checkAuthStatus()
  }, [])

  const signUp = async (email: string, password: string, userData: any) => {
    try {
      console.log('🔐 Starting registration for:', email);
      
      // TEMPORARY: Simulate successful registration without backend
      // This allows frontend testing while backend is fixed
      console.log('📤 Simulating registration data:', {
        email,
        full_name: userData.fullName,
        phone: userData.phone || null,
        location: userData.location || null
      });
      
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      console.log('✅ Registration successful! (simulated)');
      return { error: null }
      
      // ORIGINAL CODE (commented out until backend is fixed):
      /*
      // Prepare registration data for backend
      const registrationData = {
        email,
        password,
        full_name: userData.fullName,
        phone: userData.phone || null,
        location: userData.location || null
      }

      console.log('📤 Sending registration data:', registrationData);
      const response = await apiService.registerUser(registrationData)
      console.log('📥 Registration response:', response);
      
      if (response.success) {
        console.log('✅ Registration successful!');
        return { error: null }
      } else {
        console.log('❌ Registration failed:', response.message);
        return { error: { message: response.message } }
      }
      */
    } catch (error: any) {
      console.error('💥 Registration error:', error)
      return { error: { message: error.message || 'Registration failed' } }
    }
  }

  const signIn = async (email: string, password: string) => {
    try {
      const response = await apiService.loginUser({ email, password })
      
      if (response.success && response.data) {
        const { user, access_token, refresh_token } = response.data
        
        // Store tokens
        localStorage.setItem('access_token', access_token)
        localStorage.setItem('refresh_token', refresh_token)
        
        // Update state
        setUser(user)
        setSession({ access_token, refresh_token })
        
        return { error: null }
      } else {
        return { error: { message: response.message || 'Login failed' } }
      }
    } catch (error: any) {
      console.error('Login error:', error)
      return { error: { message: error.message || 'Login failed' } }
    }
  }

  const signOut = async () => {
    try {
      const token = localStorage.getItem('access_token')
      if (token) {
        await apiService.logoutUser(token)
      }
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      // Clear local storage and state
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      setUser(null)
      setSession(null)
    }
  }

  const resetPassword = async (email: string) => {
    try {
      // For now, we'll just return success since the backend doesn't have password reset yet
      // You can implement this later
      return { error: null }
    } catch (error: any) {
      console.error('Password reset error:', error)
      return { error: { message: error.message || 'Password reset failed' } }
    }
  }

  const value = {
    user,
    session,
    loading,
    signUp,
    signIn,
    signOut,
    resetPassword,
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}
