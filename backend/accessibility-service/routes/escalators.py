"""
Escalator endpoints
"""
from flask import Blueprint, jsonify, request
from models import db, Escalator
from utils.helpers import format_response, format_error

escalators_bp = Blueprint('escalators', __name__, url_prefix='/api/accessibility/escalators')

@escalators_bp.route('', methods=['GET'])
def get_all_escalators():
    """Get all escalators with optional filtering"""
    status = request.args.get('status')
    station_id = request.args.get('station_id')
    
    query = Escalator.query
    
    if status:
        query = query.filter_by(status=status)
    if station_id:
        query = query.filter_by(station_id=station_id)
    
    escalators = query.all()
    return jsonify(format_response([e.to_dict() for e in escalators]))


@escalators_bp.route('/<escalator_id>', methods=['GET'])
def get_escalator(escalator_id):
    """Get specific escalator information"""
    escalator = Escalator.query.get(escalator_id)
    
    if not escalator:
        return jsonify(format_error(f'Escalator {escalator_id} not found', 404))
    
    return jsonify(format_response(escalator.to_dict()))
