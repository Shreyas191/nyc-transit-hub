import requests
from flask import current_app
from app import db
from app.models.service_status import ServiceStatus
from app.models.route import Route
from datetime import datetime
from google.transit import gtfs_realtime_pb2
import time

class MTAAlertsService:
    """Service to fetch and process MTA service alerts"""
    
    # MTA Alert Feed URLs
    ALERT_FEEDS = {
        'subway': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts',
        'bus_bronx': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fbus-alerts-bronx',
        'bus_brooklyn': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fbus-alerts-brooklyn',
        'bus_manhattan': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fbus-alerts-manhattan',
        'bus_queens': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fbus-alerts-queens',
        'bus_staten_island': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fbus-alerts-staten-island',
        'lirr': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Flirr-alerts',
        'metro_north': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fmetronorth-alerts',
    }
    
    @staticmethod
    def fetch_alerts(feed_type='subway'):
        """
        Fetch alerts from MTA GTFS-RT feed WITHOUT API KEY
        """
        try:
            feed_url = MTAAlertsService.ALERT_FEEDS.get(feed_type)
            if not feed_url:
                print(f"Unknown feed type: {feed_type}")
                return []

            # No API key required
            response = requests.get(feed_url, timeout=10)
            response.raise_for_status()

            # Parse protobuf feed
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)

            alerts = []
            for entity in feed.entity:
                if entity.HasField('alert'):
                    alert = MTAAlertsService._parse_alert(entity.alert, entity.id)
                    if alert:
                        alerts.append(alert)

            print(f"Fetched {len(alerts)} alerts from {feed_type}")
            return alerts

        except requests.exceptions.RequestException as e:
            print(f"Error fetching MTA alerts: {e}")
            return []
        except Exception as e:
            print(f"Error parsing MTA alerts: {e}")
            return []


    @staticmethod
    def _parse_alert(alert_data, alert_id):
        """
        Parse GTFS-RT alert into structured format
        
        Args:
            alert_data: GTFS-RT alert object
            alert_id: Alert ID from feed
        
        Returns:
            Dictionary with parsed alert information
        """
        try:
            # Extract header text
            header = ""
            if alert_data.header_text.translation:
                header = alert_data.header_text.translation[0].text
            
            # Extract description
            description = ""
            if alert_data.description_text.translation:
                description = alert_data.description_text.translation[0].text
            
            # Get affected routes
            affected_routes = []
            for informed_entity in alert_data.informed_entity:
                if informed_entity.route_id:
                    affected_routes.append(informed_entity.route_id)
            
            # Get time period
            active_period = []
            for period in alert_data.active_period:
                active_period.append({
                    'start': datetime.fromtimestamp(period.start) if period.start else None,
                    'end': datetime.fromtimestamp(period.end) if period.end else None
                })
            
            # Determine alert cause and effect
            cause = MTAAlertsService._get_cause_text(alert_data.cause)
            effect = MTAAlertsService._get_effect_text(alert_data.effect)
            
            # Determine severity based on effect
            severity = MTAAlertsService._get_severity(alert_data.effect)
            
            return {
                'id': alert_id,
                'header': header,
                'description': description,
                'affected_routes': list(set(affected_routes)),  # Remove duplicates
                'cause': cause,
                'effect': effect,
                'severity': severity,
                'active_period': active_period,
                'url': alert_data.url.translation[0].text if alert_data.url.translation else None
            }
            
        except Exception as e:
            print(f"Error parsing individual alert: {e}")
            return None
    
    @staticmethod
    def _get_cause_text(cause_enum):
        """Convert GTFS-RT cause enum to text"""
        causes = {
            1: "UNKNOWN_CAUSE",
            2: "OTHER_CAUSE",
            3: "TECHNICAL_PROBLEM",
            4: "STRIKE",
            5: "DEMONSTRATION",
            6: "ACCIDENT",
            7: "HOLIDAY",
            8: "WEATHER",
            9: "MAINTENANCE",
            10: "CONSTRUCTION",
            11: "POLICE_ACTIVITY",
            12: "MEDICAL_EMERGENCY"
        }
        return causes.get(cause_enum, "UNKNOWN_CAUSE")
    
    @staticmethod
    def _get_effect_text(effect_enum):
        """Convert GTFS-RT effect enum to text"""
        effects = {
            1: "NO_SERVICE",
            2: "REDUCED_SERVICE",
            3: "SIGNIFICANT_DELAYS",
            4: "DETOUR",
            5: "ADDITIONAL_SERVICE",
            6: "MODIFIED_SERVICE",
            7: "OTHER_EFFECT",
            8: "UNKNOWN_EFFECT",
            9: "STOP_MOVED"
        }
        return effects.get(effect_enum, "UNKNOWN_EFFECT")
    
    @staticmethod
    def _get_severity(effect_enum):
        """Determine severity level based on effect"""
        critical_effects = [1]  # NO_SERVICE
        high_effects = [3, 4]  # SIGNIFICANT_DELAYS, DETOUR
        medium_effects = [2, 6]  # REDUCED_SERVICE, MODIFIED_SERVICE
        
        if effect_enum in critical_effects:
            return "critical"
        elif effect_enum in high_effects:
            return "high"
        elif effect_enum in medium_effects:
            return "medium"
        else:
            return "low"
    
    @staticmethod
    def fetch_all_alerts():
        """Fetch alerts from all feeds"""
        all_alerts = []
        
        for feed_type in MTAAlertsService.ALERT_FEEDS.keys():
            alerts = MTAAlertsService.fetch_alerts(feed_type)
            for alert in alerts:
                alert['feed_type'] = feed_type
            all_alerts.extend(alerts)
            time.sleep(0.5)  # Rate limiting
        
        return all_alerts
    
    @staticmethod
    def update_service_status_from_alerts():
        """
        Update service status in database based on fetched alerts
        This replaces the manual status updates
        """
        try:
            # Fetch subway alerts (most common)
            alerts = MTAAlertsService.fetch_alerts('subway')
            
            # Group alerts by route
            route_alerts = {}
            for alert in alerts:
                for route_id in alert['affected_routes']:
                    if route_id not in route_alerts:
                        route_alerts[route_id] = []
                    route_alerts[route_id].append(alert)
            
            # Update status for each affected route
            for route_id, alerts_list in route_alerts.items():
                # Get the most severe alert
                most_severe = max(alerts_list, 
                                key=lambda x: ['low', 'medium', 'high', 'critical'].index(x['severity']))
                
                # Create or update service status
                status = ServiceStatus(
                    route_id=route_id,
                    status=most_severe['effect'].lower().replace('_', ' '),
                    message=most_severe['header'] or most_severe['description'],
                    severity=most_severe['severity'],
                    timestamp=datetime.utcnow()
                )
                
                db.session.add(status)
            
            # Mark routes with no alerts as good service
            all_routes = Route.query.all()
            for route in all_routes:
                if route.id not in route_alerts:
                    status = ServiceStatus(
                        route_id=route.id,
                        status='good_service',
                        message='No delays',
                        severity='low',
                        timestamp=datetime.utcnow()
                    )
                    db.session.add(status)
            
            db.session.commit()
            print(f"Updated service status for {len(route_alerts)} routes with alerts")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error updating service status from alerts: {e}")

