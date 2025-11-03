"""
Route planning endpoints
"""
from flask import Blueprint, jsonify, request
from services.route_planner import route_planner
from utils.helpers import format_response, format_error

routes_bp = Blueprint('routes', __name__, url_prefix='/api/accessibility')

@routes_bp.route('/route', methods=['GET'])
def plan_accessible_route():
    """Plan accessible route between two stations"""
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    
    if not origin or not destination:
        return jsonify(format_error('Both origin and destination parameters are required'))
    
    route = route_planner.find_accessible_route(origin, destination)
    
    if not route:
        return jsonify(format_error('Could not find one or both stations'))
    
    return jsonify(format_response(route))


@routes_bp.route('/alternatives/<station_id>', methods=['GET'])
def get_alternatives(station_id):
    """Find nearby accessible alternatives for a station"""
    max_distance = float(request.args.get('max_distance', 0.5))
    
    from services.mta_client import mta_client
    from services.cache_manager import cache
    
    # Get station info
    stations = cache.get('stations_data')
    if not stations:
        stations = mta_client.fetch_stations()
    
    station = None
    for s in stations:
        if s['station_id'] == station_id:
            station = s
            break
    
    if not station:
        return jsonify(format_error(f'Station {station_id} not found', 404))
    
    # Get equipment status for this station
    equipment = cache.get('equipment_data')
    if not equipment:
        equipment = mta_client.fetch_equipment_status()
    
    station_elevators = [e for e in equipment.get('elevators', []) 
                        if e['station_id'] == station_id]
    working_elevators = [e for e in station_elevators if e['status'] == 'active']
    
    # Find alternatives
    alternatives = route_planner.find_nearby_accessible_stations(
        station_id, 
        station.get('latitude'), 
        station.get('longitude'),
        max_distance
    )
    
    return jsonify(format_response({
        'station': {
            **station,
            'is_accessible': len(working_elevators) > 0,
            'working_elevators': len(working_elevators),
            'total_elevators': len(station_elevators)
        },
        'alternatives': alternatives,
        'search_radius_km': max_distance
    }))

