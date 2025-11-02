"""
Elevator endpoints
"""
from flask import Blueprint, jsonify, request
from models import db, Elevator
from utils.helpers import format_response, format_error

elevators_bp = Blueprint('elevators', __name__, url_prefix='/api/accessibility/elevators')

@elevators_bp.route('', methods=['GET'])
def get_all_elevators():
    """Get all elevators with optional status filtering"""
    status = request.args.get('status')
    station_id = request.args.get('station_id')
    
    query = Elevator.query
    
    if status:
        query = query.filter_by(status=status)
    if station_id:
        query = query.filter_by(station_id=station_id)
    
    elevators = query.all()
    return jsonify(format_response([e.to_dict() for e in elevators]))


@elevators_bp.route('/<elevator_id>', methods=['GET'])
def get_elevator(elevator_id):
    """Get specific elevator information"""
    elevator = Elevator.query.get(elevator_id)
    
    if not elevator:
        return jsonify(format_error(f'Elevator {elevator_id} not found', 404))
    
    return jsonify(format_response(elevator.to_dict()))


@elevators_bp.route('/outages', methods=['GET'])
def get_outages():
    """Get all current elevator outages"""
    outages = Elevator.query.filter_by(status='outage').all()
    return jsonify(format_response([e.to_dict() for e in outages]))
