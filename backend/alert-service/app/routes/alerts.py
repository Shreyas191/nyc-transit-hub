from datetime import datetime
from flask import Blueprint, jsonify, request
from app.services.mta_alerts_service import MTAAlertsService
from app.services.cache_service import CacheService

alerts_bp = Blueprint('alerts', __name__)

@alerts_bp.route('/', methods=['GET'])
def get_all_alerts():
    """Get all current MTA service alerts"""
    # Try cache first
    cached = CacheService.get('mta_alerts_all')
    if cached:
        return jsonify(cached)
    
    # Fetch from MTA
    alerts = MTAAlertsService.fetch_all_alerts()
    
    # Cache for 2 minutes
    CacheService.set('mta_alerts_all', alerts, timeout=120)
    
    return jsonify(alerts)

@alerts_bp.route('/subway', methods=['GET'])
def get_subway_alerts():
    """Get subway service alerts"""
    cached = CacheService.get('mta_alerts_subway')
    if cached:
        return jsonify(cached)
    
    alerts = MTAAlertsService.fetch_alerts('subway')
    CacheService.set('mta_alerts_subway', alerts, timeout=120)
    
    return jsonify(alerts)

@alerts_bp.route('/route/<route_id>', methods=['GET'])
def get_route_alerts(route_id):
    """Get alerts for specific route"""
    # Fetch all subway alerts
    alerts = MTAAlertsService.fetch_alerts('subway')
    
    # Filter by route
    route_alerts = [
        alert for alert in alerts 
        if route_id in alert['affected_routes']
    ]
    
    return jsonify(route_alerts)

@alerts_bp.route('/active', methods=['GET'])
def get_active_alerts():
    """Get only currently active alerts"""
    alerts = MTAAlertsService.fetch_all_alerts()
    now = datetime.utcnow()
    
    active_alerts = []
    for alert in alerts:
        # Check if alert is currently active
        is_active = False
        if not alert['active_period']:
            is_active = True  # No time restriction
        else:
            for period in alert['active_period']:
                start = period['start']
                end = period['end']
                
                if start and end:
                    if start <= now <= end:
                        is_active = True
                        break
                elif start:
                    if start <= now:
                        is_active = True
                        break
                elif end:
                    if now <= end:
                        is_active = True
                        break
        
        if is_active:
            active_alerts.append(alert)
    
    return jsonify(active_alerts)