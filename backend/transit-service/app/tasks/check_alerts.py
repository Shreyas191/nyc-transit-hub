import requests
from app import db
from app.models.alert import Alert
from app.services.notification_service import NotificationService
from flask import current_app
from datetime import datetime, timedelta

class AlertChecker:
    @staticmethod
    def check_all_alerts():
        """Check all active alerts against current transit status"""
        print(f"Checking alerts at {datetime.utcnow()}")
        
        # Get all active alerts
        active_alerts = Alert.query.filter_by(is_active=True).all()
        
        if not active_alerts:
            print("No active alerts to check")
            return
        
        # Group alerts by item (route/station) to minimize API calls
        items_to_check = {}
        for alert in active_alerts:
            key = f"{alert.item_type}:{alert.item_id}"
            if key not in items_to_check:
                items_to_check[key] = []
            items_to_check[key].append(alert)
        
        # Check status for each unique item
        for item_key, alerts in items_to_check.items():
            item_type, item_id = item_key.split(':')
            AlertChecker.check_item_status(item_type, item_id, alerts)
    
    @staticmethod
    def check_item_status(item_type, item_id, alerts):
        """Check status for a specific route/station and notify users"""
        try:
            # Fetch current status from Transit Service
            transit_url = current_app.config['TRANSIT_SERVICE_URL']
            
            if item_type == 'route':
                response = requests.get(
                    f"{transit_url}/api/status/{item_id}",
                    timeout=5
                )
            else:  # station
                response = requests.get(
                    f"{transit_url}/api/stations/{item_id}",
                    timeout=5
                )
            
            if response.status_code != 200:
                print(f"Error fetching status for {item_type} {item_id}")
                return
            
            status_data = response.json()
            
            # Analyze status and send notifications if needed
            AlertChecker.process_status_and_notify(status_data, alerts)
            
        except Exception as e:
            print(f"Error checking status for {item_type} {item_id}: {e}")
    
    @staticmethod
    def process_status_and_notify(status_data, alerts):
        """Process status data and send notifications to relevant users"""
        # Extract status information
        if 'current_status' in status_data:
            current_status = status_data['current_status']
            status_type = current_status.get('status', 'good_service')
            message = current_status.get('message', '')
            severity = current_status.get('severity', 'low')
        else:
            return
        
        # Check if this status warrants notifications
        if status_type == 'good_service':
            return  # No need to notify for good service
        
        # Send notifications to all users with matching alerts
        for alert in alerts:
            # Check if user should be notified based on alert_type
            if AlertChecker.should_notify(alert, status_type):
                # Check notification limits
                if not NotificationService.check_notification_limit(alert.firebase_uid):
                    print(f"User {alert.firebase_uid} has reached notification limit")
                    continue
                
                # Create notification message
                notification_message = AlertChecker.create_notification_message(
                    alert,
                    status_type,
                    message
                )
                
                # Send notification
                NotificationService.send_notification(
                    firebase_uid=alert.firebase_uid,
                    message=notification_message,
                    severity=severity,
                    alert_id=alert.id
                )
    
    @staticmethod
    def should_notify(alert, status_type):
        """Determine if alert should trigger notification based on type"""
        alert_type_mapping = {
            'delay': ['delays'],
            'service_change': ['service_change', 'delays'],
            'planned_work': ['planned_work'],
            'cancellation': ['service_change']
        }
        
        allowed_statuses = alert_type_mapping.get(alert.alert_type, [])
        return status_type in allowed_statuses
    
    @staticmethod
    def create_notification_message(alert, status_type, message):
        """Create user-friendly notification message"""
        item_name = alert.item_name or alert.item_id
        
        if alert.item_type == 'route':
            prefix = f"Alert for {item_name} line"
        else:
            prefix = f"Alert for {item_name} station"
        
        return f"{prefix}: {message}"

