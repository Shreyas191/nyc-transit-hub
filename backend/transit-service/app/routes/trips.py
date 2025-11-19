from flask import Blueprint, jsonify
from app.services.realtime_service import RealtimeService
from datetime import datetime

trips_bp = Blueprint('trips', __name__)

@trips_bp.route('/<trip_id>', methods=['GET'])
def get_trip_details(trip_id):
    """Get details and real-time updates for a specific trip"""
    # Try all feeds to find this trip
    feeds = ['123456S', 'ACE', 'BDFM', 'G', 'JZ', 'NQRW', 'L', '7']
    
    for feed_id in feeds:
        updates = RealtimeService.fetch_trip_updates(feed_id)
        
        for update in updates:
            if update['trip_id'] == trip_id:
                return jsonify({
                    'trip_id': trip_id,
                    'route_id': update['route_id'],
                    'vehicle_id': update['vehicle_id'],
                    'stops': update['stop_time_updates'],
                    'timestamp': datetime.utcnow().isoformat()
                })
    
    return jsonify({'error': 'Trip not found'}), 404
