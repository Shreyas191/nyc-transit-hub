from flask import Blueprint, jsonify, request
from app.services.realtime_service import RealtimeService
from app.services.cache_service import CacheService
from datetime import datetime

realtime_bp = Blueprint('realtime', __name__)

@realtime_bp.route('/trains', methods=['GET'])
def get_all_trains():
    """Get all train positions across all feeds"""
    # Try cache first
    cached = CacheService.get('all_train_positions')
    if cached:
        return jsonify(cached)
    
    all_positions = []
    feeds = ['123456S', 'ACE', 'BDFM', 'G', 'JZ', 'NQRW', 'L', '7']
    
    for feed_id in feeds:
        positions = RealtimeService.fetch_train_positions(feed_id)
        all_positions.extend(positions)
    
    # Cache for 30 seconds
    result = {
        'trains': all_positions,
        'count': len(all_positions),
        'timestamp': datetime.utcnow().isoformat()
    }
    
    CacheService.set('all_train_positions', result, timeout=30)
    
    return jsonify(result)

@realtime_bp.route('/route/<route_id>', methods=['GET'])
def get_trains_by_route(route_id):
    """Get train positions for specific route"""
    # Determine which feed to use
    feed_id = RealtimeService.get_feed_for_route(route_id)
    
    if not feed_id:
        return jsonify({'error': f'Unknown route: {route_id}'}), 404
    
    # Try cache
    cache_key = f'train_positions_{route_id}'
    cached = CacheService.get(cache_key)
    if cached:
        return jsonify(cached)
    
    # Fetch positions
    positions = RealtimeService.fetch_train_positions(feed_id)
    
    # Filter by route
    route_positions = [
        pos for pos in positions 
        if pos['route_id'] == route_id.upper()
    ]
    
    result = {
        'route_id': route_id,
        'trains': route_positions,
        'count': len(route_positions),
        'timestamp': datetime.utcnow().isoformat()
    }
    
    CacheService.set(cache_key, result, timeout=30)
    
    return jsonify(result)

@realtime_bp.route('/feed/<feed_id>', methods=['GET'])
def get_trains_by_feed(feed_id):
    """Get all trains in a specific feed"""
    positions = RealtimeService.fetch_train_positions(feed_id)
    
    return jsonify({
        'feed_id': feed_id,
        'trains': positions,
        'count': len(positions),
        'timestamp': datetime.utcnow().isoformat()
    })

@realtime_bp.route('/station/<station_id>', methods=['GET'])
def get_trains_at_station(station_id):
    """Get trains currently at or approaching a station"""
    # Get all train positions
    all_positions = []
    feeds = ['123456S', 'ACE', 'BDFM', 'G', 'JZ', 'NQRW', 'L', '7']
    
    for feed_id in feeds:
        positions = RealtimeService.fetch_train_positions(feed_id)
        all_positions.extend(positions)
    
    # Filter trains at this station
    station_trains = [
        pos for pos in all_positions
        if pos['current_stop'] and station_id in pos['current_stop']
    ]
    
    return jsonify({
        'station_id': station_id,
        'trains': station_trains,
        'count': len(station_trains),
        'timestamp': datetime.utcnow().isoformat()
    })

@realtime_bp.route('/arrivals/<station_id>', methods=['GET'])
def get_station_arrivals(station_id):
    """Get upcoming arrivals at a station"""
    route_id = request.args.get('route')
    
    # Get feed(s) to check
    if route_id:
        feed_id = RealtimeService.get_feed_for_route(route_id)
        if not feed_id:
            return jsonify({'error': f'Unknown route: {route_id}'}), 404
        feeds = [feed_id]
    else:
        feeds = ['123456S', 'ACE', 'BDFM', 'G', 'JZ', 'NQRW', 'L', '7']
    
    # Fetch trip updates
    all_arrivals = []
    for feed_id in feeds:
        updates = RealtimeService.fetch_trip_updates(feed_id)
        
        for update in updates:
            for stop_time in update['stop_time_updates']:
                if stop_time['stop_id'] and station_id in stop_time['stop_id']:
                    if stop_time['arrival']:
                        all_arrivals.append({
                            'route_id': update['route_id'],
                            'trip_id': update['trip_id'],
                            'vehicle_id': update['vehicle_id'],
                            'stop_id': stop_time['stop_id'],
                            'arrival_time': stop_time['arrival'].isoformat(),
                            'minutes_until_arrival': int(
                                (stop_time['arrival'] - datetime.utcnow()).total_seconds() / 60
                            )
                        })
    
    # Sort by arrival time
    all_arrivals.sort(key=lambda x: x['arrival_time'])
    
    # Only show upcoming arrivals
    upcoming = [a for a in all_arrivals if a['minutes_until_arrival'] >= 0]
    
    return jsonify({
        'station_id': station_id,
        'arrivals': upcoming[:10],  # Next 10 trains
        'count': len(upcoming),
        'timestamp': datetime.utcnow().isoformat()
    })