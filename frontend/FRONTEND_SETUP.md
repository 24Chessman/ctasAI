# 🎨 Frontend Setup Guide for CTAS AI

## 📋 Prerequisites

- Backend server running on `http://localhost:8000`
- Node.js and npm/yarn installed
- Supabase database set up (already done)

## 🚀 Step 1: Configure Frontend Environment

### 1.1 Create Environment File
Create `frontend/.env` with:

```bash
# Backend API URL
VITE_API_URL=http://localhost:8000/api/v1

# Supabase Configuration (for reference)
VITE_SUPABASE_URL=https://bdxchhewjbfzydeyjces.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJkeGNoaGV3amJmenlkZXlqY2VzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTY1MDA1NTUsImV4cCI6MjA3MjA3NjU1NX0.t58O9RpsmRPv7_5jJFSxJkzHX2hIt0jsgrFXUHGOSb0
```

### 1.2 Install Dependencies
```bash
cd frontend
npm install
```

## 🔧 Step 2: What's Been Updated

### 2.1 New API Service
- **File**: `src/services/api.ts`
- **Purpose**: Handles all communication with the backend API
- **Features**: Authentication, user management, notifications

### 2.2 Updated AuthContext
- **File**: `src/contexts/AuthContext.tsx`
- **Changes**: Now uses backend API instead of Supabase directly
- **Benefits**: Better security, centralized authentication

### 2.3 Simplified Registration Form
- **File**: `src/components/auth/RegistrationPage.tsx`
- **Changes**: Streamlined form with only essential fields
- **Fields**: Email, password, full name, phone, location, role

## 🧪 Step 3: Test the Setup

### 3.1 Start Frontend
```bash
cd frontend
npm run dev
```

### 3.2 Test Registration
1. Go to `http://localhost:5173/register`
2. Fill out the registration form
3. Click "Create Account"
4. Check backend logs for registration attempt

### 3.3 Check Backend Logs
Look for these messages in your backend terminal:
- "User registered successfully: [email]"
- "Supabase client initialized successfully"

## 🚨 Troubleshooting

### Common Issues

#### 1. "Failed to fetch" Error
**Cause**: Backend server not running or CORS issue
**Solution**: 
- Ensure backend is running on port 8000
- Check CORS configuration in backend
- Verify API URL in frontend .env file

#### 2. "User already exists" Error
**Cause**: Email already registered in database
**Solution**: 
- Use a different email address
- Check Supabase dashboard for existing users

#### 3. "Database connection failed" Error
**Cause**: Supabase not properly configured
**Solution**:
- Verify Supabase setup script ran successfully
- Check backend logs for connection errors
- Ensure environment variables are correct

### Debug Steps

1. **Check Backend Status**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **Check Frontend Console**:
   - Open browser DevTools
   - Look for network errors
   - Check console for error messages

3. **Verify Environment Variables**:
   ```bash
   # In frontend directory
   echo $VITE_API_URL
   ```

## ✅ Success Criteria

Your frontend setup is complete when:

1. ✅ Frontend starts without errors
2. ✅ Registration form loads correctly
3. ✅ Form submission reaches backend
4. ✅ User gets created in Supabase database
5. ✅ Success message appears after registration

## 🔗 Next Steps

After successful setup:

1. **Test Login**: Try logging in with the registered user
2. **Test Notifications**: Use the notification testing features
3. **Customize UI**: Modify the form fields and styling as needed
4. **Add Features**: Implement additional functionality

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review backend logs for detailed error messages
3. Check browser console for frontend errors
4. Verify all environment variables are set correctly
5. Ensure both frontend and backend are running

---

**Happy coding! 🚀**
