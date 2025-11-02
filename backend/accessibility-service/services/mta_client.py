"""
Real MTA API client for fetching live equipment and station data
"""
import requests
import csv
from io import StringIO
from datetime import datetime
from services.cache_manager import cache

class MTAClient:
    def __init__(self):
        self.equipment_url = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fnyct_ene.json'
        self.stations_url = 'http://web.mta.info/developers/data/nyct/subway/Stations.csv'
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AccessibilityService/1.0'
        })
    
    def fetch_equipment_status(self):
        """
        Fetch real-time equipment status from MTA
        Returns dict with elevators and escalators
        """
        try:
            print(f"[{datetime.utcnow()}] Fetching equipment status from MTA...")
            response = self.session.get(self.equipment_url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            equipment_data = self._parse_equipment_data(data)
            
            # Cache the results
            cache.set('equipment_data', equipment_data, ttl=600)
            print(f"[{datetime.utcnow()}] Equipment data fetched successfully")
            
            return equipment_data
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching equipment data: {str(e)}")
            # Return cached data if available
            cached = cache.get('equipment_data')
            if cached:
                print("Returning cached equipment data")
                return cached
            return {'elevators': [], 'escalators': [], 'error': str(e)}
    
    def _parse_equipment_data(self, data):
        """Parse MTA equipment JSON response"""
        elevators = []
        escalators = []
        
        # MTA equipment feed structure
        if isinstance(data, dict):
            # Check for equipment array or direct equipment data
            equipment_list = data.get('equipment', [])
            
            if not equipment_list and isinstance(data, list):
                equipment_list = data
            
            for item in equipment_list:
                equipment_type = item.get('equipmenttype', '').lower()
                
                equipment_info = {
                    'id': item.get('equipmentno', item.get('equipment_id', 'UNKNOWN')),
                    'station_id': item.get('station', item.get('stationid', 'UNKNOWN')),
                    'station_name': item.get('stationname', item.get('station_name', 'Unknown Station')),
                    'borough': item.get('borough', 'Unknown'),
                    'status': self._parse_status(item.get('outageStatus', item.get('isactive', 'Active'))),
                    'location': item.get('serving', item.get('location', 'Unknown Location')),
                    'ada': item.get('ada', True),
                    'outage_start': item.get('outageStartDate'),
                    'outage_end': item.get('outageEndDate'),
                    'estimated_return': item.get('estimatedReturnToService'),
                    'reason': item.get('reason', ''),
                    'updated_at': datetime.utcnow().isoformat()
                }
                
                if 'elevator' in equipment_type or 'el' == equipment_type:
                    elevators.append(equipment_info)
                elif 'escalator' in equipment_type or 'es' == equipment_type:
                    equipment_info['direction'] = item.get('direction', 'bidirectional')
                    escalators.append(equipment_info)
        
        return {
            'elevators': elevators,
            'escalators': escalators,
            'last_updated': datetime.utcnow().isoformat(),
            'total_elevators': len(elevators),
            'total_escalators': len(escalators)
        }
    
    def _parse_status(self, status_value):
        """Parse equipment status from MTA format"""
        if isinstance(status_value, str):
            status_lower = status_value.lower()
            if 'outage' in status_lower or 'out' in status_lower:
                return 'outage'
            elif 'active' in status_lower or 'in service' in status_lower:
                return 'active'
            elif 'maintenance' in status_lower:
                return 'maintenance'
        return 'active'
    
    def fetch_stations(self):
        """
        Fetch station data from MTA Stations CSV
        Returns list of stations with accessibility info
        """
        try:
            print(f"[{datetime.utcnow()}] Fetching stations from MTA...")
            response = self.session.get(self.stations_url, timeout=30)
            response.raise_for_status()
            
            stations = self._parse_stations_csv(response.text)
            
            # Cache the results
            cache.set('stations_data', stations, ttl=3600)  # Cache for 1 hour
            print(f"[{datetime.utcnow()}] Stations data fetched successfully: {len(stations)} stations")
            
            return stations
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching stations data: {str(e)}")
            # Return cached data if available
            cached = cache.get('stations_data')
            if cached:
                print("Returning cached stations data")
                return cached
            return []
    
    def _parse_stations_csv(self, csv_text):
        """Parse MTA stations CSV data"""
        stations = []
        csv_reader = csv.DictReader(StringIO(csv_text))
        
        for row in csv_reader:
            # MTA CSV columns: Station ID, Complex ID, GTFS Stop ID, Division, Line, Stop Name, Borough, 
            # Daytime Routes, Structure, GTFS Latitude, GTFS Longitude, North Direction Label, 
            # South Direction Label, ADA, ADA Notes
            
            station_id = row.get('GTFS Stop ID', row.get('Station ID', ''))
            
            station = {
                'station_id': station_id,
                'station_name': row.get('Stop Name', 'Unknown'),
                'borough': row.get('Borough', 'Unknown'),
                'lines': row.get('Daytime Routes', '').split(),
                'latitude': float(row.get('GTFS Latitude', 0)) if row.get('GTFS Latitude') else None,
                'longitude': float(row.get('GTFS Longitude', 0)) if row.get('GTFS Longitude') else None,
                'ada_compliant': self._parse_ada(row.get('ADA', '0')),
                'ada_notes': row.get('ADA Notes', ''),
                'structure': row.get('Structure', 'Unknown'),
                'complex_id': row.get('Complex ID', ''),
            }
            
            stations.append(station)
        
        return stations
    
    def _parse_ada(self, ada_value):
        """Parse ADA compliance value"""
        if isinstance(ada_value, str):
            return ada_value.strip() in ['1', 'True', 'true', 'YES', 'Yes', 'yes']
        return bool(ada_value)


# Global MTA client instance
mta_client = MTAClient()