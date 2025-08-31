import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from contextlib import asynccontextmanager
import threading
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import predict, data, alerts, evacuation, auth, sms
from app.automation.scheduler import start_scheduler

# Load environment variables from the backend/.env file
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(env_path)

# Check if environment variables are loaded
print("Environment variables loaded:")
print("SUPABASE_URL:", "SET" if os.getenv("SUPABASE_URL") else "MISSING")
print("SUPABASE_KEY:", "SET" if os.getenv("SUPABASE_KEY") else "MISSING")
print("SMTP_USERNAME:", "SET" if os.getenv("SMTP_USERNAME") else "MISSING")
print("SMTP_PASSWORD:", "SET" if os.getenv("SMTP_PASSWORD") else "MISSING")
print("SMS_API_KEY:", "SET" if os.getenv("SMS_API_KEY") else "MISSING")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the scheduler in a separate thread when the app starts
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()
    print("Automated prediction scheduler started")
    
    yield
    
    # Clean up when the app stops
    print("Shutting down scheduler")

app = FastAPI(
    title="CTAS AI - Coastal Threat Alert System",
    description="API for detecting cyclones and managing coastal threat alerts",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Add your frontend origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(predict.router, prefix="/api/v1", tags=["prediction"])
app.include_router(data.router, prefix="/api/v1", tags=["data"])
app.include_router(alerts.router, prefix="/api/v1", tags=["alerts"])
app.include_router(evacuation.router, prefix="/api/v1/evacuation", tags=["evacuation"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(sms.router, prefix="/api/v1/sms", tags=["sms"])

@app.get("/")
async def root():
    return {
        "message": "CTAS AI - Coastal Threat Alert System",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "auth": "/api/v1/auth",
            "alerts": "/api/v1/alerts",
            "prediction": "/api/v1/prediction",
            "data": "/api/v1/data",
            "evacuation": "/api/v1/evacuation",
            "sms": "/api/v1/sms"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "System is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)