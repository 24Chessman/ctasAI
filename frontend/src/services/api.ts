// frontend/src/services/api.ts
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

console.log('🌐 API Service: Using base URL:', API_BASE_URL);
console.log('🌐 API Service: Environment VITE_API_URL:', import.meta.env.VITE_API_URL);

export interface UserRegistrationData {
  email: string;
  password: string;
  full_name: string;
  phone?: string;
  location?: string;
}

export interface UserLoginData {
  email: string;
  password: string;
}

export interface UserProfile {
  id: string;
  email: string;
  full_name: string;
  phone?: string;
  location?: string;
  role: string;
  created_at: string;
  updated_at: string;
}

export interface AuthResponse {
  success: boolean;
  message: string;
  data?: any;
}

class ApiService {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    console.log('🌐 Making API request to:', url);
    console.log('🌐 Request options:', options);
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      console.log('🌐 Response status:', response.status);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('🌐 Error response:', errorData);
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('🌐 Response data:', data);
      return data;
    } catch (error) {
      console.error('🌐 API request failed:', error);
      throw error;
    }
  }

  // Authentication endpoints
  async registerUser(userData: UserRegistrationData): Promise<AuthResponse> {
    return this.request<AuthResponse>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async loginUser(loginData: UserLoginData): Promise<AuthResponse> {
    return this.request<AuthResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(loginData),
    });
  }

  async logoutUser(token: string): Promise<AuthResponse> {
    return this.request<AuthResponse>('/auth/logout', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
  }

  async getUserProfile(token: string): Promise<AuthResponse> {
    return this.request<AuthResponse>('/auth/profile', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
  }

  async updateUserProfile(
    token: string,
    profileData: Partial<UserProfile>
  ): Promise<AuthResponse> {
    return this.request<AuthResponse>('/auth/profile', {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(profileData),
    });
  }

  async changePassword(
    token: string,
    currentPassword: string,
    newPassword: string
  ): Promise<AuthResponse> {
    return this.request<AuthResponse>('/auth/change-password', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        current_password: currentPassword,
        new_password: newPassword,
      }),
    });
  }

  async deleteUser(token: string): Promise<AuthResponse> {
    return this.request<AuthResponse>('/auth/profile', {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
  }

  async verifyToken(token: string): Promise<AuthResponse> {
    return this.request<AuthResponse>('/auth/verify', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
  }

  // Alert endpoints
  async testNotification(
    token: string,
    notificationData: {
      threat_level: string;
      cyclone_probability: number;
      storm_surge_level: string;
      water_level: number;
      test_email?: string;
    }
  ): Promise<AuthResponse> {
    return this.request<AuthResponse>('/alerts/test-notification', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(notificationData),
    });
  }

  async testAlertSystem(token: string): Promise<AuthResponse> {
    return this.request<AuthResponse>('/alerts/test-alert-system', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
  }

  async getUsers(token: string): Promise<AuthResponse> {
    return this.request<AuthResponse>('/alerts/users', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
  }

  // Health check
  async healthCheck(): Promise<{ status: string; message: string }> {
    return this.request<{ status: string; message: string }>('/health', {
      method: 'GET',
    });
  }
}

export const apiService = new ApiService();
export default apiService;
