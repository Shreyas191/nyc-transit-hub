from flask import Blueprint, jsonify, request
from app.models.route import Route
from app.services.cache_service import CacheService

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/', methods=['GET'])
def get_all_routes():
    """Get all transit routes"""
    # Try cache first
    cached = CacheService.get('all_routes')
    if cached:
        return jsonify(cached)
    
    routes = Route.query.all()
    result = [route.to_dict() for route in routes]
    
    # Cache for 5 minutes
    CacheService.set('all_routes', result, timeout=300)
    
    return jsonify(result)

@routes_bp.route('/<route_id>', methods=['GET'])
def get_route(route_id):
    """Get specific route details"""
    route = Route.query.get_or_404(route_id)
    return jsonify(route.to_dict())

@routes_bp.route('/<route_id>/stations', methods=['GET'])
def get_route_stations(route_id):
    """Get all stations for a specific route"""
    # This would query the route_stations junction table
    # Simplified for this example
    return jsonify({
        'route_id': route_id,
        'stations': []
    })
