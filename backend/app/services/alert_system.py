# backend/app/services/alert_system.py
import logging
from datetime import datetime
from app.services.notification_service import notification_service

logger = logging.getLogger(__name__)

def check_and_send_alerts(prediction, weather_data):
    """
    Check if prediction requires sending alerts and send them
    """
    try:
        alerts = []
        
        # Check cyclone threat
        cyclone_data = prediction.get('cyclone', {})
        if (cyclone_data.get('classification') == 'CYCLONE' and 
            cyclone_data.get('probability', 0) >= 0.7):
            alerts.append({
                "type": "cyclone",
                "severity": "high",
                "message": f"Cyclone threat detected with {cyclone_data.get('probability', 0)*100:.1f}% probability",
                "data": cyclone_data
            })
        
        # Check storm surge threat
        surge_data = prediction.get('storm_surge', {})
        surge_threat = surge_data.get('threat_level', 'low')
        if surge_threat in ["high", "extreme"]:
            alerts.append({
                "type": "storm_surge",
                "severity": surge_threat,
                "message": f"Storm surge threat: {surge_threat}. Estimated water level: {surge_data.get('total_water_level', 0):.2f}m",
                "data": surge_data
            })
        
        # Check overall threat level
        overall_threat = prediction.get('overall_threat', 'low')
        if overall_threat in ["HIGH", "high", "extreme"] and alerts:
            # Send evacuation alerts to users
            logger.warning(f"🚨 HIGH THREAT DETECTED: Sending evacuation alerts to users")
            
            # Send evacuation notification to all users
            notification_result = notification_service.send_evacuation_alert(prediction)
            
            if notification_result["success"]:
                logger.warning(f"✅ EVACUATION ALERTS SENT: {notification_result['message']}")
            else:
                logger.error(f"❌ FAILED TO SEND EVACUATION ALERTS: {notification_result['message']}")
            
            # Also send traditional alerts
            for alert in alerts:
                send_alert(alert, weather_data)
            logger.warning(f"ALERTS SENT: {len(alerts)} alerts triggered")
        elif alerts:
            logger.info(f"Threats detected but below threshold: {[a['type'] for a in alerts]}")
        else:
            logger.info("No threats detected")
            
    except Exception as e:
        logger.error(f"Error in alert system: {e}")

def send_alert(alert_data, weather_data):
    """
    Send alert to appropriate channels
    """
    try:
        alert_message = f"""
        COASTAL THREAT ALERT - {alert_data['type'].upper()}
        
        Threat Level: {alert_data['severity'].upper()}
        Detection Time: {datetime.now()}
        
        Details:
        {alert_data['message']}
        
        Current Conditions:
        - Wind Speed: {weather_data.get('wind_speed', 0)} km/h
        - Pressure: {weather_data.get('pressure', 0)} hPa
        - Water Level: {alert_data['data'].get('total_water_level', 0)} m
        
        TAKE NECESSARY PRECAUTIONS!
        """
        
        logger.warning(alert_message)
        
        # Here you would add code to actually send the alert via:
        # SMS, Email, Push Notifications, etc.
        
    except Exception as e:
        logger.error(f"Error sending alert: {e}")