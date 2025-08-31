# 🔐 Login Troubleshooting Guide

## Problem Description
When you enter credentials and hit "Sign In", the form buffers indefinitely and nothing happens.

## 🔍 Step-by-Step Troubleshooting

### Step 1: Check Backend Server Status

**Start the backend server:**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 2: Test Backend Connectivity

**Run the server test:**
```bash
python quick_server_test.py
```

**Expected output:**
```
🚀 Quick Server Test
==============================
🔍 Testing server accessibility...
   Trying: http://localhost:8000/docs
   ✅ Success! Status: 200

✅ Server is accessible!

🔐 Testing login endpoint...
   Status: 401
   Response: {"detail":"Invalid credentials"}

🎉 Login endpoint is working!
```

### Step 3: Check Frontend Configuration

**Verify frontend environment variables:**
Create or check `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_SUPABASE_URL=https://bdxchhewjbfzydeyjces.supabase.co
VITE_SUPABASE_ANON_KEY=your-supabase-anon-key
```

### Step 4: Check Browser Console

**Open browser developer tools (F12) and check:**
1. **Console tab** - Look for JavaScript errors
2. **Network tab** - Check if API requests are being made
3. **Application tab** - Check if tokens are being stored

**Common errors to look for:**
- CORS errors
- Network timeout errors
- JavaScript syntax errors
- API endpoint not found errors

### Step 5: Test API Endpoints Manually

**Test login endpoint with curl:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

**Expected response:**
```json
{
  "detail": "Invalid credentials"
}
```

### Step 6: Check Database Connection

**Run database connection test:**
```bash
python test_db_connection.py
```

**Expected output:**
```
✅ Supabase client initialized successfully
✅ Profiles table exists and is accessible
✅ Email column exists in profiles table
```

## 🚨 Common Issues and Solutions

### Issue 1: Backend Server Not Starting
**Symptoms:** Server fails to start or shows errors
**Solutions:**
1. Check if port 8000 is already in use
2. Verify all dependencies are installed
3. Check environment variables

### Issue 2: CORS Errors
**Symptoms:** Browser console shows CORS errors
**Solutions:**
1. Verify CORS configuration in `app/main.py`
2. Check if frontend URL is in allowed origins
3. Restart both frontend and backend servers

### Issue 3: Network Timeout
**Symptoms:** Requests timeout or hang
**Solutions:**
1. Check firewall settings
2. Verify server is bound to correct interface
3. Test with different ports

### Issue 4: Database Connection Issues
**Symptoms:** Backend can't connect to Supabase
**Solutions:**
1. Verify Supabase credentials
2. Check SSL configuration
3. Test database connection directly

### Issue 5: Frontend Not Making Requests
**Symptoms:** No network requests in browser dev tools
**Solutions:**
1. Check API_BASE_URL configuration
2. Verify JavaScript is loading correctly
3. Check for JavaScript errors

## 🔧 Debug Commands

### Test Backend Import
```bash
python -c "from app.main import app; print('✅ Backend app imported successfully')"
```

### Test Auth Service
```bash
python -c "from app.services.auth_service import auth_service; print('✅ Auth service initialized')"
```

### Test Database Connection
```bash
python test_db_connection.py
```

### Test Login Endpoint
```bash
python test_login_debug.py
```

## 📋 Checklist

- [ ] Backend server is running on port 8000
- [ ] Server is accessible via localhost
- [ ] Login endpoint responds (even with 401)
- [ ] Frontend environment variables are set
- [ ] No CORS errors in browser console
- [ ] Network requests are being made
- [ ] Database connection is working
- [ ] No JavaScript errors in console

## 🎯 Quick Fix Steps

1. **Restart Backend:**
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Restart Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Clear Browser Cache:**
   - Open DevTools (F12)
   - Right-click refresh button
   - Select "Empty Cache and Hard Reload"

4. **Check Environment Variables:**
   - Verify `VITE_API_URL` in frontend `.env`
   - Verify Supabase credentials in backend `.env`

5. **Test with Known User:**
   - Register a new user first
   - Try logging in with the registered credentials

## 🆘 Still Having Issues?

If the problem persists:

1. **Check server logs** for any error messages
2. **Verify network connectivity** between frontend and backend
3. **Test with a different browser** to rule out browser-specific issues
4. **Check if antivirus/firewall** is blocking connections
5. **Try running on different ports** if 8000 is blocked

## 📞 Getting Help

When seeking help, provide:
1. Backend server logs
2. Browser console errors
3. Network tab screenshots
4. Environment configuration (without sensitive data)
5. Steps to reproduce the issue
