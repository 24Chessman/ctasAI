#!/usr/bin/env python3
"""
Quick Start Script for CTAS AI Backend
This script helps you get the backend running quickly
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'fastapi', 'uvicorn', 'pydantic', 'python-dotenv', 
        'supabase', 'pandas', 'numpy', 'scikit-learn', 'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ All packages installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please run: pip install -r requirements.txt")
            return False
    
    return True

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path('.env')
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    print("📝 Creating .env file...")
    
    env_content = """# Supabase Configuration
SUPABASE_URL=https://bdxchhewjbfzydeyjces.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJkeGNoaGV3amJmenlkZXlqY2VzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTY1MDA1NTUsImV4cCI6MjA3MjA3NjU1NX0.t58O9RpsmRPv7_5jJFSxJkzHX2hIt0jsgrFXUHGOSb0

# Email Configuration (Optional - for sending notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# SMS Configuration (Optional)
SMS_API_KEY=your-sms-api-key
SMS_API_URL=your-sms-api-url

# Push Notification Configuration (Optional)
PUSH_API_KEY=your-push-api-key
PUSH_API_URL=your-push-api-url
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully")
        print("⚠️  Please update the email/SMS configuration if needed")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def check_supabase_setup():
    """Check if Supabase setup script exists"""
    setup_file = Path('supabase_setup.sql')
    
    if setup_file.exists():
        print("✅ Supabase setup script found")
        print("📋 Please run this script in your Supabase SQL Editor:")
        print(f"   File: {setup_file.absolute()}")
        return True
    else:
        print("❌ Supabase setup script not found")
        return False

def start_server():
    """Start the FastAPI server"""
    print("\n🚀 Starting FastAPI server...")
    print("📖 Server will be available at: http://localhost:8000")
    print("📖 API documentation at: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, '-m', 'uvicorn', 
            'app.main:app', 
            '--reload', 
            '--host', '0.0.0.0', 
            '--port', '8000'
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")

def main():
    """Main function"""
    print("🚀 CTAS AI Backend Quick Start")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return
    
    print()
    
    # Check dependencies
    if not check_dependencies():
        return
    
    print()
    
    # Create .env file
    if not create_env_file():
        return
    
    print()
    
    # Check Supabase setup
    if not check_supabase_setup():
        return
    
    print()
    
    # Instructions
    print("📋 Setup Instructions:")
    print("1. Run the Supabase setup script in your Supabase dashboard")
    print("2. Update .env file with your email/SMS credentials (optional)")
    print("3. The server will start automatically")
    print()
    
    # Ask user if they want to start the server
    response = input("🤔 Do you want to start the server now? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        start_server()
    else:
        print("\n📝 To start the server later, run:")
        print("   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        print("\n📝 To test the setup, run:")
        print("   python test_database_setup.py")

if __name__ == "__main__":
    main()
