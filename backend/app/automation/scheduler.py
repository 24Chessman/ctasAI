# backend/app/automation/scheduler.py
import schedule
import time
import logging
import threading
from datetime import datetime
from app.services.threat_detection import run_threat_detection
from app.services.alert_system import check_and_send_alerts

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def prediction_job():
    """
    Job that runs every minute to fetch data and make predictions
    """
    try:
        logger.info(f"Running prediction job at {datetime.now()}")
        
        # Run threat detection
        threat_data = run_threat_detection()
        
        # Check if we need to send alerts
        check_and_send_alerts(threat_data, threat_data.get("weather_data", {}))
        
    except Exception as e:
        logger.error(f"Error in prediction job: {e}")

def scheduler_worker():
    """
    Worker function that runs the scheduler loop
    """
    try:
        # Schedule the job to run every minute
        schedule.every(1).minutes.do(prediction_job)
        
        # Run immediately on startup
        prediction_job()
        
        logger.info("Coastal threat scheduler started. Running predictions every 1 minutes.")
        
        # Keep the scheduler running
        while True:
            schedule.run_pending()
            time.sleep(1)
            
    except Exception as e:
        logger.error(f"Error in scheduler worker: {e}")

def start_scheduler():
    """
    Start the scheduled job to run every minute in a background thread
    """
    try:
        # Create and start the scheduler thread
        scheduler_thread = threading.Thread(target=scheduler_worker, daemon=True)
        scheduler_thread.start()
        logger.info("Scheduler thread started successfully")
        
    except Exception as e:
        logger.error(f"Error starting scheduler: {e}")