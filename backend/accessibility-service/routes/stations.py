"""
Station accessibility endpoints
"""
from flask import Blueprint, request, jsonify
from services.mta_client import mta_client
from services.cache_manager import cache
from utils.helpers import format_response, format_error

stations_bp = Blueprint('stations', __name__, url_prefix='/api/accessibility/stations')

@stations_bp.route('', methods=['GET'])
def get_all_stations():
    """Get all stations with accessibility information"""
    ada_only = request.args.get('ada_only', 'false').lower() == 'true'
    accessible_only = request.args.get('accessible_only', 'false').lower() == 'true'
    
    # Get stations from cache or MTA
    stations = cache.get('stations_data')
    if not stations:
        stations = mta_client.fetch_stations()
    
    if not stations:
        return jsonify(format_error('Unable to fetch stations data', 503))
    
    # Get equipment data for accessibility check
    equipment = cache.get('equipment_data')
    if not equipment:
        equipment = mta_client.fetch_equipment_status()
    
    results = []
    for station in stations:
        # Filter by ADA compliance if requested
        if ada_only and not station.get('ada_compliant'):
            continue
        
        # Check real-time accessibility
        station_elevators = [e for e in equipment.get('elevators', []) 
                            if e['station_id'] == station['station_id']]
        working_elevators = [e for e in station_elevators if e['status'] == 'active']
        
        station_data = {
            **station,
            'has_elevator': len(station_elevators) > 0,
            'elevator_count': len(station_elevators),
            'working_elevators': len(working_elevators),
            'is_currently_accessible': len(working_elevators) > 0
        }
        
        # Filter by current accessibility if requested
        if accessible_only and not station_data['is_currently_accessible']:
            continue
        
        results.append(station_data)
    
    return jsonify(format_response(results, f"Found {len(results)} stations"))


@stations_bp.route('/<station_id>', methods=['GET'])
def get_station(station_id):
    """Get detailed accessibility information for a specific station"""
    # Get stations
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
    
    # Get equipment for this station
    equipment = cache.get('equipment_data')
    if not equipment:
        equipment = mta_client.fetch_equipment_status()
    
    station_elevators = [e for e in equipment.get('elevators', []) 
                        if e['station_id'] == station_id]
    station_escalators = [e for e in equipment.get('escalators', []) 
                         if e['station_id'] == station_id]
    
    working_elevators = [e for e in station_elevators if e['status'] == 'active']
    working_escalators = [e for e in station_escalators if e['status'] == 'active']
    
    station_data = {
        **station,
        'equipment': {
            'elevators': station_elevators,
            'escalators': station_escalators,
            'working_elevators_count': len(working_elevators),
            'working_escalators_count': len(working_escalators)
        },
        'is_currently_accessible': len(working_elevators) > 0
    }
    
    return jsonify(format_response(station_data))

