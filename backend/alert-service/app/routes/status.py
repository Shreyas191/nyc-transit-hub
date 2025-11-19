from flask import Blueprint, jsonify
from app.models.service_status import ServiceStatus
from app.models.route import Route
from sqlalchemy import desc

status_bp = Blueprint('status', __name__)

@status_bp.route('/', methods=['GET'])
def get_all_status():
    """Get current status for all routes"""
    routes = Route.query.all()
    result = []
    
    for route in routes:
        # Get latest status for each route
        latest_status = ServiceStatus.query.filter_by(
            route_id=route.id
        ).order_by(desc(ServiceStatus.timestamp)).first()
        
        route_dict = route.to_dict()
        route_dict['current_status'] = latest_status.to_dict() if latest_status else {
            'status': 'good_service',
            'message': 'No delays',
            'severity': 'low'
        }
        
        result.append(route_dict)
    
    return jsonify(result)

@status_bp.route('/<route_id>', methods=['GET'])
def get_route_status(route_id):
    """Get status history for specific route"""
    route = Route.query.get_or_404(route_id)
    
    # Get recent statuses (last 24 hours)
    statuses = ServiceStatus.query.filter_by(
        route_id=route_id
    ).order_by(desc(ServiceStatus.timestamp)).limit(50).all()
    
    return jsonify({
        'route': route.to_dict(),
        'status_history': [status.to_dict() for status in statuses]
    })
