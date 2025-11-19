import requests
from flask import current_app
from google.transit import gtfs_realtime_pb2
from datetime import datetime


class RealtimeService:
    """Service to fetch and process real-time train positions"""
    
    @staticmethod
    def get_feed_for_route(route_id):
        """Determine which feed contains this route"""
        route_to_feed = {
            '1': '123456S', '2': '123456S', '3': '123456S',
            '4': '123456S', '5': '123456S', '6': '123456S', 'S': '123456S',
            'A': 'ACE', 'C': 'ACE', 'E': 'ACE',
            'B': 'BDFM', 'D': 'BDFM', 'F': 'BDFM', 'M': 'BDFM',
            'G': 'G',
            'J': 'JZ', 'Z': 'JZ',
            'N': 'NQRW', 'Q': 'NQRW', 'R': 'NQRW', 'W': 'NQRW',
            'L': 'L',
            '7': '7',
            'SI': 'SIR',
        }
        return route_to_feed.get(route_id.upper())
    
    @staticmethod
    def fetch_train_positions(feed_id):
        """
        Fetch real-time train positions from MTA GTFS-RT feed
        
        Args:
            feed_id: Feed identifier (e.g., '123456S', 'ACE', 'L')
        
        Returns:
            List of train position dictionaries
        """
        try:
            # Get feed URL
            feeds = current_app.config['MTA_FEEDS']
            feed_url_suffix = feeds.get(feed_id)
            if not feed_url_suffix:
                print(f"Unknown feed ID: {feed_id}")
                return []
            
            # Construct full URL
            base_url = current_app.config['MTA_API_BASE_URL']
            url = f"{base_url}/{feed_url_suffix}"
            
            # Fetch the GTFS-RT feed (no API key required)
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse the protobuf data
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)
            
            # Extract vehicle positions
            positions = []
            for entity in feed.entity:
                if entity.HasField('vehicle'):
                    position = RealtimeService._parse_vehicle_position(entity.vehicle)
                    if position:
                        positions.append(position)
            
            print(f"Fetched {len(positions)} train positions from {feed_id}")
            return positions
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching train positions: {e}")
            return []
        except Exception as e:
            print(f"Error parsing train positions: {e}")
            return []
    
    @staticmethod
    def _parse_vehicle_position(vehicle):
        """Parse GTFS-RT vehicle position into structured format"""
        try:
            position = None
            if vehicle.HasField('position'):
                position = {
                    'latitude': vehicle.position.latitude,
                    'longitude': vehicle.position.longitude,
                    'bearing': vehicle.position.bearing if vehicle.position.HasField('bearing') else None
                }
            
            # Get trip information
            trip_id = vehicle.trip.trip_id if vehicle.trip.HasField('trip_id') else None
            route_id = vehicle.trip.route_id if vehicle.trip.HasField('route_id') else None
            
            # Get current stop
            current_stop = vehicle.stop_id if vehicle.HasField('stop_id') else None
            
            # Get status
            current_status = RealtimeService._get_status_text(
                vehicle.current_status if vehicle.HasField('current_status') else None
            )
            
            # Get timestamp
            timestamp = datetime.fromtimestamp(vehicle.timestamp) if vehicle.HasField('timestamp') else datetime.utcnow()
            
            return {
                'vehicle_id': vehicle.vehicle.id if vehicle.vehicle.HasField('id') else None,
                'trip_id': trip_id,
                'route_id': route_id,
                'position': position,
                'current_stop': current_stop,
                'status': current_status,
                'timestamp': timestamp,
                'congestion_level': RealtimeService._get_congestion_text(
                    vehicle.congestion_level if vehicle.HasField('congestion_level') else None
                ),
                'occupancy_status': RealtimeService._get_occupancy_text(
                    vehicle.occupancy_status if vehicle.HasField('occupancy_status') else None
                )
            }
            
        except Exception as e:
            print(f"Error parsing vehicle position: {e}")
            return None
    
    @staticmethod
    def _get_status_text(status_enum):
        """Convert GTFS-RT vehicle status enum to text"""
        statuses = {
            0: "INCOMING_AT",
            1: "STOPPED_AT",
            2: "IN_TRANSIT_TO"
        }
        return statuses.get(status_enum, "UNKNOWN")
    
    @staticmethod
    def _get_congestion_text(congestion_enum):
        """Convert congestion level enum to text"""
        levels = {
            0: "UNKNOWN",
            1: "RUNNING_SMOOTHLY",
            2: "STOP_AND_GO",
            3: "CONGESTION",
            4: "SEVERE_CONGESTION"
        }
        return levels.get(congestion_enum, "UNKNOWN")
    
    @staticmethod
    def _get_occupancy_text(occupancy_enum):
        """Convert occupancy status enum to text"""
        statuses = {
            0: "EMPTY",
            1: "MANY_SEATS_AVAILABLE",
            2: "FEW_SEATS_AVAILABLE",
            3: "STANDING_ROOM_ONLY",
            4: "CRUSHED_STANDING_ROOM_ONLY",
            5: "FULL",
            6: "NOT_ACCEPTING_PASSENGERS"
        }
        return statuses.get(occupancy_enum, "UNKNOWN")
    
    @staticmethod
    def fetch_trip_updates(feed_id):
        """
        Fetch trip updates (arrival/departure predictions)
        
        Args:
            feed_id: Feed identifier
        
        Returns:
            List of trip update dictionaries
        """
        try:
            feeds = current_app.config['MTA_FEEDS']
            feed_url_suffix = feeds.get(feed_id)
            if not feed_url_suffix:
                return []
            
            base_url = current_app.config['MTA_API_BASE_URL']
            url = f"{base_url}/{feed_url_suffix}"
            
            # Fetch the GTFS-RT feed (no API key required)
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)
            
            updates = []
            for entity in feed.entity:
                if entity.HasField('trip_update'):
                    update = RealtimeService._parse_trip_update(entity.trip_update)
                    if update:
                        updates.append(update)
            
            return updates
            
        except Exception as e:
            print(f"Error fetching trip updates: {e}")
            return []
    
    @staticmethod
    def _parse_trip_update(trip_update):
        """Parse GTFS-RT trip update"""
        try:
            trip_id = trip_update.trip.trip_id if trip_update.trip.HasField('trip_id') else None
            route_id = trip_update.trip.route_id if trip_update.trip.HasField('route_id') else None
            
            # Parse stop time updates
            stop_times = []
            for stop_time in trip_update.stop_time_update:
                stop_info = {
                    'stop_id': stop_time.stop_id if stop_time.HasField('stop_id') else None,
                    'arrival': None,
                    'departure': None
                }
                
                if stop_time.HasField('arrival'):
                    stop_info['arrival'] = datetime.fromtimestamp(stop_time.arrival.time)
                
                if stop_time.HasField('departure'):
                    stop_info['departure'] = datetime.fromtimestamp(stop_time.departure.time)
                
                stop_times.append(stop_info)
            
            return {
                'trip_id': trip_id,
                'route_id': route_id,
                'stop_time_updates': stop_times,
                'vehicle_id': trip_update.vehicle.id if trip_update.vehicle.HasField('id') else None
            }
            
        except Exception as e:
            print(f"Error parsing trip update: {e}")
            return None
