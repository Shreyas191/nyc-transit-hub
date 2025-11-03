"""
Accessible route planning service
Plans routes using only accessible stations with working equipment
"""
from services.cache_manager import cache
from services.mta_client import mta_client
from utils.helpers import calculate_distance

class RoutePlannerService:
    def __init__(self):
        pass
    
    def find_accessible_route(self, origin_id, destination_id):
        """
        Plan accessible route between two stations
        Returns route information with accessibility status
        """
        stations = self._get_stations()
        equipment = self._get_equipment()
        
        origin = self._find_station(origin_id, stations)
        destination = self._find_station(destination_id, stations)
        
        if not origin or not destination:
            return None
        
        # Check accessibility status
        origin_status = self._check_station_accessibility(origin_id, equipment)
        dest_status = self._check_station_accessibility(destination_id, equipment)
        
        route = {
            'origin': {
                **origin,
                'accessibility': origin_status
            },
            'destination': {
                **destination,
                'accessibility': dest_status
            },
            'route_fully_accessible': origin_status['is_accessible'] and dest_status['is_accessible'],
            'recommendations': []
        }
        
        # Add alternatives if needed
        if not origin_status['is_accessible']:
            route['origin_alternatives'] = self.find_nearby_accessible_stations(
                origin_id, origin.get('latitude'), origin.get('longitude')
            )
        
        if not dest_status['is_accessible']:
            route['destination_alternatives'] = self.find_nearby_accessible_stations(
                destination_id, destination.get('latitude'), destination.get('longitude')
            )
        
        return route
    
    def find_nearby_accessible_stations(self, exclude_station_id, lat, lon, max_distance=0.5):
        """Find nearby accessible stations within max_distance (km)"""
        if not lat or not lon:
            return []
        
        stations = self._get_stations()
        equipment = self._get_equipment()
        nearby = []
        
        for station in stations:
            if station['station_id'] == exclude_station_id:
                continue
            
            s_lat = station.get('latitude')
            s_lon = station.get('longitude')
            
            if not s_lat or not s_lon:
                continue
            
            distance = calculate_distance(lat, lon, s_lat, s_lon)
            
            if distance <= max_distance:
                accessibility = self._check_station_accessibility(station['station_id'], equipment)
                
                if accessibility['is_accessible']:
                    nearby.append({
                        'station': station,
                        'accessibility': accessibility,
                        'distance_km': round(distance, 2),
                        'walking_time_minutes': round(distance * 12)  # ~12 min per km
                    })
        
        # Sort by distance
        nearby.sort(key=lambda x: x['distance_km'])
        return nearby[:5]  # Return top 5
    
    def _get_stations(self):
        """Get stations from cache or fetch from MTA"""
        stations = cache.get('stations_data')
        if not stations:
            stations = mta_client.fetch_stations()
        return stations or []
    
    def _get_equipment(self):
        """Get equipment data from cache or fetch from MTA"""
        equipment = cache.get('equipment_data')
        if not equipment:
            equipment = mta_client.fetch_equipment_status()
        return equipment
    
    def _find_station(self, station_id, stations):
        """Find station by ID"""
        for station in stations:
            if station['station_id'] == station_id:
                return station
        return None
    
    def _check_station_accessibility(self, station_id, equipment):
        """Check if station is currently accessible"""
        elevators = [e for e in equipment.get('elevators', []) 
                     if e['station_id'] == station_id]
        
        working_elevators = [e for e in elevators if e['status'] == 'active']
        outage_elevators = [e for e in elevators if e['status'] == 'outage']
        
        return {
            'is_accessible': len(working_elevators) > 0,
            'has_elevators': len(elevators) > 0,
            'total_elevators': len(elevators),
            'working_elevators': len(working_elevators),
            'outage_elevators': len(outage_elevators),
            'elevators': elevators,
            'outages': outage_elevators
        }


# Global route planner instance
route_planner = RoutePlannerService()
