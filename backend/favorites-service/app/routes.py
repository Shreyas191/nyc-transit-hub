from flask import request, jsonify
import requests
from google.transit import gtfs_realtime_pb2
from config import Config
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_gtfs_feed(url):
    feed = gtfs_realtime_pb2.FeedMessage()
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        feed.ParseFromString(response.content)
        return feed
    except Exception as e:
        logger.error(f"Error fetching GTFS feed {url}: {e}")
        return None

def timestamp_to_iso(ts):
    if ts is None:
        return None
    if hasattr(ts, 'seconds'):
        return datetime.fromtimestamp(ts.seconds).isoformat()
    if isinstance(ts, int):
        return datetime.fromtimestamp(ts).isoformat()
    return None

def register_routes(app, db, Favorite, verify_token):

    @app.route('/api/favorites', methods=['GET'])
    @verify_token
    def get_favorites():
        uid = request.firebase_uid
        favs = Favorite.query.filter_by(firebase_uid=uid, item_type='station').all()
        return jsonify([{
            'id': f.id,
            'item_type': f.item_type,
            'item_id': f.item_id,
            'item_name': f.item_name,
            'custom_note': f.custom_note,
            'created_at': f.created_at.isoformat()
        } for f in favs] or [])

    @app.route('/api/favorites', methods=['POST'])
    @verify_token
    def add_favorite():
        data = request.get_json()
        uid = request.firebase_uid
        exists = Favorite.query.filter_by(firebase_uid=uid, item_id=data['item_id'], item_type='station').first()
        if exists:
            return jsonify({'message':'Favorite already exists'}), 400
        fav = Favorite(
            firebase_uid=uid,
            item_type='station',
            item_id=data['item_id'],
            item_name=data['item_name'],
            custom_note=data.get('custom_note')
        )
        db.session.add(fav)
        db.session.commit()
        return jsonify({'message':'Favorite added','id':fav.id})

    @app.route('/api/favorites/<int:fid>', methods=['PUT'])
    @verify_token
    def update_favorite(fid):
        data = request.get_json()
        uid = request.firebase_uid
        fav = Favorite.query.filter_by(id=fid, firebase_uid=uid, item_type='station').first()
        if not fav:
            return jsonify({'message':'Favorite not found'}), 404
        if 'custom_note' in data:
            fav.custom_note = data['custom_note']
        db.session.commit()
        return jsonify({'message':'Favorite updated'})

    @app.route('/api/favorites/<int:fid>', methods=['DELETE'])
    @verify_token
    def delete_favorite(fid):
        uid = request.firebase_uid
        fav = Favorite.query.filter_by(id=fid, firebase_uid=uid, item_type='station').first()
        if not fav:
            return jsonify({'message':'Favorite not found'}), 404
        db.session.delete(fav)
        db.session.commit()
        return jsonify({'message':'Favorite deleted'})

    @app.route('/api/favorites/routes', methods=['GET'])
    @verify_token
    def get_route_favorites():
        uid = request.firebase_uid
        favs = Favorite.query.filter_by(firebase_uid=uid, item_type='route').all()
        return jsonify([{
            'id': f.id,
            'item_type': f.item_type,
            'item_id': f.item_id,
            'item_name': f.item_name,
            'route_id': f.route_id,
            'custom_note': f.custom_note,
            'created_at': f.created_at.isoformat()
        } for f in favs] or [])

    @app.route('/api/favorites/routes', methods=['POST'])
    @verify_token
    def add_route_favorite():
        data = request.get_json()
        uid = request.firebase_uid
        if 'route_id' not in data or 'item_name' not in data:
            return jsonify({'message':'route_id and item_name required'}), 400
        exists = Favorite.query.filter_by(firebase_uid=uid, item_id=data['route_id'], item_type='route').first()
        if exists:
            return jsonify({'message':'Route favorite already exists'}), 400
        fav = Favorite(
            firebase_uid=uid,
            item_type='route',
            item_id=data['route_id'],
            item_name=data['item_name'],
            route_id=data['route_id'],
            custom_note=data.get('custom_note')
        )
        db.session.add(fav)
        db.session.commit()
        return jsonify({'message':'Route favorite added','id':fav.id})

    @app.route('/api/favorites/routes/<int:fid>', methods=['DELETE'])
    @verify_token
    def delete_route_favorite(fid):
        uid = request.firebase_uid
        fav = Favorite.query.filter_by(id=fid, firebase_uid=uid, item_type='route').first()
        if not fav:
            return jsonify({'message':'Route favorite not found'}), 404
        db.session.delete(fav)
        db.session.commit()
        return jsonify({'message':'Route favorite deleted'})

    @app.route('/api/favorites_with_realtime', methods=['GET'])
    @verify_token
    def favorites_with_realtime():
        uid = request.firebase_uid
        favs = Favorite.query.filter_by(firebase_uid=uid).all()
        combined_result = []

        for f in favs:
            realtime_data = []
            for url in Config.GTFS_FEEDS:
                feed = fetch_gtfs_feed(url)
                if feed:
                    for entity in feed.entity:
                        if entity.HasField('trip_update'):
                            for stu in entity.trip_update.stop_time_update:
                                if f.item_type == 'station' and stu.stop_id == f.item_id:
                                    realtime_data.append({
                                        'trip_id': entity.trip_update.trip.trip_id,
                                        'route_id': entity.trip_update.trip.route_id,
                                        'arrival': timestamp_to_iso(getattr(stu,'arrival',None)),
                                        'departure': timestamp_to_iso(getattr(stu,'departure',None))
                                    })
                                if f.item_type == 'route' and entity.trip_update.trip.route_id == f.route_id:
                                    realtime_data.append({
                                        'stop_id': stu.stop_id,
                                        'trip_id': entity.trip_update.trip.trip_id,
                                        'route_id': entity.trip_update.trip.route_id,
                                        'arrival': timestamp_to_iso(getattr(stu,'arrival',None)),
                                        'departure': timestamp_to_iso(getattr(stu,'departure',None))
                                    })
            combined_result.append({
                'id': f.id,
                'item_type': f.item_type,
                'item_id': f.item_id,
                'item_name': f.item_name,
                'custom_note': f.custom_note,
                'created_at': f.created_at.isoformat(),
                'realtime_updates': realtime_data
            })

        return jsonify(combined_result or [])