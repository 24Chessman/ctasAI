// Simple test script to verify frontend-backend connection
// Run this in your browser console or as a Node.js script

const API_BASE_URL = 'http://localhost:8000/api/v1';

async function testBackendConnection() {
  console.log('🧪 Testing Backend Connection...');
  
  try {
    // Test 1: Health check
    console.log('1. Testing health check...');
    const healthResponse = await fetch(`${API_BASE_URL.replace('/api/v1', '')}/health`);
    if (healthResponse.ok) {
      const healthData = await healthResponse.json();
      console.log('   ✅ Health check passed:', healthData);
    } else {
      console.log('   ❌ Health check failed:', healthResponse.status);
    }
    
    // Test 2: Root endpoint
    console.log('2. Testing root endpoint...');
    const rootResponse = await fetch(`${API_BASE_URL.replace('/api/v1', '')}/`);
    if (rootResponse.ok) {
      const rootData = await rootResponse.json();
      console.log('   ✅ Root endpoint working:', rootData.message);
      console.log('   Available endpoints:', rootData.endpoints);
    } else {
      console.log('   ❌ Root endpoint failed:', rootResponse.status);
    }
    
    // Test 3: Auth endpoints
    console.log('3. Testing auth endpoints...');
    const authResponse = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: 'test@example.com',
        password: 'testpassword123',
        full_name: 'Test User',
        phone: '+1234567890',
        location: 'coastal_zone_1'
      })
    });
    
    if (authResponse.ok) {
      const authData = await authResponse.json();
      console.log('   ✅ Registration endpoint working:', authData.message);
    } else {
      const errorData = await authResponse.json().catch(() => ({}));
      console.log('   ❌ Registration endpoint failed:', authResponse.status, errorData.detail);
    }
    
    // Test 4: Alerts endpoints
    console.log('4. Testing alerts endpoints...');
    const alertsResponse = await fetch(`${API_BASE_URL}/alerts/`);
    if (alertsResponse.ok) {
      const alertsData = await alertsResponse.json();
      console.log('   ✅ Alerts endpoint working:', alertsData.message);
    } else {
      console.log('   ❌ Alerts endpoint failed:', alertsResponse.status);
    }
    
  } catch (error) {
    console.error('❌ Connection test failed:', error.message);
    
    if (error.message.includes('fetch')) {
      console.log('💡 This usually means:');
      console.log('   - Backend server is not running');
      console.log('   - CORS is not configured properly');
      console.log('   - Network connectivity issues');
    }
  }
}

// Run the test
testBackendConnection();

// Export for use in other contexts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { testBackendConnection };
}
