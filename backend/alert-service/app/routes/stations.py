from flask import Blueprint, jsonify, request
from app.models.station import Station
from sqlalchemy import func
import math

stations_bp = Blueprint('stations', __name__)

@stations_bp.route('/', methods=['GET'])
def get_all_stations():
    """Get all stations"""
    stations = Station.query.all()
    return jsonify([station.to_dict() for station in stations])

@stations_bp.route('/<station_id>', methods=['GET'])
def get_station(station_id):
    """Get specific station details"""
    station = Station.query.get_or_404(station_id)
    return jsonify(station.to_dict())

@stations_bp.route('/nearby', methods=['GET'])
def get_nearby_stations():
    """Find stations near given coordinates"""
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    radius = request.args.get('radius', default=0.5, type=float)  # km
    
    if not lat or not lon:
        return jsonify({'error': 'Latitude and longitude required'}), 400
    
    # Simple distance calculation (Haversine formula would be more accurate)
    stations = Station.query.all()
    nearby = []
    
    for station in stations:
        if station.latitude and station.longitude:
            distance = calculate_distance(lat, lon, station.latitude, station.longitude)
            if distance <= radius:
                station_dict = station.to_dict()
                station_dict['distance'] = round(distance, 2)
                nearby.append(station_dict)
    
    # Sort by distance
    nearby.sort(key=lambda x: x['distance'])
    
    return jsonify(nearby)

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in km"""
    R = 6371  # Earth's radius in km
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    
    c = 2 * math.asin(math.sqrt(a))
    return R * c