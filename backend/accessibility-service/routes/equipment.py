"""
Equipment endpoints for elevators and escalators
"""
from flask import Blueprint, jsonify, request
from services.mta_client import mta_client
from services.cache_manager import cache
from utils.helpers import format_response, format_error

equipment_bp = Blueprint('equipment', __name__, url_prefix='/api/accessibility')

@equipment_bp.route('/elevators', methods=['GET'])
def get_all_elevators():
    """Get all elevators with real-time status"""
    status_filter = request.args.get('status')
    station_id = request.args.get('station_id')
    
    # Get equipment data
    equipment = cache.get('equipment_data')
    if not equipment:
        equipment = mta_client.fetch_equipment_status()
    
    elevators = equipment.get('elevators', [])
    
    # Apply filters
    if status_filter:
        elevators = [e for e in elevators if e['status'] == status_filter]
    
    if station_id:
        elevators = [e for e in elevators if e['station_id'] == station_id]
    
    return jsonify(format_response({
        'elevators': elevators,
        'count': len(elevators),
        'last_updated': equipment.get('last_updated')
    }))


@equipment_bp.route('/elevators/<elevator_id>', methods=['GET'])
def get_elevator(elevator_id):
    """Get specific elevator information"""
    equipment = cache.get('equipment_data')
    if not equipment:
        equipment = mta_client.fetch_equipment_status()
    
    elevator = None
    for e in equipment.get('elevators', []):
        if e['id'] == elevator_id:
            elevator = e
            break
    
    if not elevator:
        return jsonify(format_error(f'Elevator {elevator_id} not found', 404))
    
    return jsonify(format_response(elevator))


@equipment_bp.route('/elevators/outages', methods=['GET'])
def get_elevator_outages():
    """Get all current elevator outages"""
    equipment = cache.get('equipment_data')
    if not equipment:
        equipment = mta_client.fetch_equipment_status()
    
    outages = [e for e in equipment.get('elevators', []) if e['status'] == 'outage']
    
    return jsonify(format_response({
        'outages': outages,
        'count': len(outages),
        'last_updated': equipment.get('last_updated')
    }))


@equipment_bp.route('/escalators', methods=['GET'])
def get_all_escalators():
    """Get all escalators with real-time status"""
    status_filter = request.args.get('status')
    station_id = request.args.get('station_id')
    
    equipment = cache.get('equipment_data')
    if not equipment:
        equipment = mta_client.fetch_equipment_status()
    
    escalators = equipment.get('escalators', [])
    
    # Apply filters
    if status_filter:
        escalators = [e for e in escalators if e['status'] == status_filter]
    
    if station_id:
        escalators = [e for e in escalators if e['station_id'] == station_id]
    
    return jsonify(format_response({
        'escalators': escalators,
        'count': len(escalators),
        'last_updated': equipment.get('last_updated')
    }))


@equipment_bp.route('/escalators/<escalator_id>', methods=['GET'])
def get_escalator(escalator_id):
    """Get specific escalator information"""
    equipment = cache.get('equipment_data')
    if not equipment:
        equipment = mta_client.fetch_equipment_status()
    
    escalator = None
    for e in equipment.get('escalators', []):
        if e['id'] == escalator_id:
            escalator = e
            break
    
    if not escalator:
        return jsonify(format_error(f'Escalator {escalator_id} not found', 404))
    
    return jsonify(format_response(escalator))
