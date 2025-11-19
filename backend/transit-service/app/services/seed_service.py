from app import db
from app.models.route import Route
from app.models.station import Station

def seed_initial_data():
    """Seed database with NYC Subway data"""
    
    # Check if already seeded
    if Route.query.first():
        return
    
    print("Seeding initial data...")
    
    # NYC Subway Routes
    routes_data = [
        {'id': '1', 'name': '1', 'type': 'subway', 'color': '#EE352E', 'text_color': '#FFFFFF', 'feed_id': '123456S'},
        {'id': '2', 'name': '2', 'type': 'subway', 'color': '#EE352E', 'text_color': '#FFFFFF', 'feed_id': '123456S'},
        {'id': '3', 'name': '3', 'type': 'subway', 'color': '#EE352E', 'text_color': '#FFFFFF', 'feed_id': '123456S'},
        {'id': '4', 'name': '4', 'type': 'subway', 'color': '#00933C', 'text_color': '#FFFFFF', 'feed_id': '123456S'},
        {'id': '5', 'name': '5', 'type': 'subway', 'color': '#00933C', 'text_color': '#FFFFFF', 'feed_id': '123456S'},
        {'id': '6', 'name': '6', 'type': 'subway', 'color': '#00933C', 'text_color': '#FFFFFF', 'feed_id': '123456S'},
        {'id': 'A', 'name': 'A', 'type': 'subway', 'color': '#0039A6', 'text_color': '#FFFFFF', 'feed_id': 'ACE'},
        {'id': 'C', 'name': 'C', 'type': 'subway', 'color': '#0039A6', 'text_color': '#FFFFFF', 'feed_id': 'ACE'},
        {'id': 'E', 'name': 'E', 'type': 'subway', 'color': '#0039A6', 'text_color': '#FFFFFF', 'feed_id': 'ACE'},
        {'id': 'B', 'name': 'B', 'type': 'subway', 'color': '#FF6319', 'text_color': '#FFFFFF', 'feed_id': 'BDFM'},
        {'id': 'D', 'name': 'D', 'type': 'subway', 'color': '#FF6319', 'text_color': '#FFFFFF', 'feed_id': 'BDFM'},
        {'id': 'F', 'name': 'F', 'type': 'subway', 'color': '#FF6319', 'text_color': '#FFFFFF', 'feed_id': 'BDFM'},
        {'id': 'M', 'name': 'M', 'type': 'subway', 'color': '#FF6319', 'text_color': '#FFFFFF', 'feed_id': 'BDFM'},
        {'id': 'G', 'name': 'G', 'type': 'subway', 'color': '#6CBE45', 'text_color': '#FFFFFF', 'feed_id': 'G'},
        {'id': 'J', 'name': 'J', 'type': 'subway', 'color': '#996633', 'text_color': '#FFFFFF', 'feed_id': 'JZ'},
        {'id': 'Z', 'name': 'Z', 'type': 'subway', 'color': '#996633', 'text_color': '#FFFFFF', 'feed_id': 'JZ'},
        {'id': 'L', 'name': 'L', 'type': 'subway', 'color': '#A7A9AC', 'text_color': '#FFFFFF', 'feed_id': 'L'},
        {'id': 'N', 'name': 'N', 'type': 'subway', 'color': '#FCCC0A', 'text_color': '#000000', 'feed_id': 'NQRW'},
        {'id': 'Q', 'name': 'Q', 'type': 'subway', 'color': '#FCCC0A', 'text_color': '#000000', 'feed_id': 'NQRW'},
        {'id': 'R', 'name': 'R', 'type': 'subway', 'color': '#FCCC0A', 'text_color': '#000000', 'feed_id': 'NQRW'},
        {'id': 'W', 'name': 'W', 'type': 'subway', 'color': '#FCCC0A', 'text_color': '#000000', 'feed_id': 'NQRW'},
        {'id': '7', 'name': '7', 'type': 'subway', 'color': '#B933AD', 'text_color': '#FFFFFF', 'feed_id': '7'},
        {'id': 'S', 'name': 'S (Shuttle)', 'type': 'subway', 'color': '#808183', 'text_color': '#FFFFFF', 'feed_id': '123456S'},
    ]
    
    for route_data in routes_data:
        route = Route(**route_data)
        db.session.add(route)
    
    # Major NYC Subway Stations
    stations_data = [
        {'id': '127', 'name': 'Times Square-42 St', 'latitude': 40.7580, 'longitude': -73.9855, 'accessible': True, 'borough': 'Manhattan'},
        {'id': '631', 'name': 'Grand Central-42 St', 'latitude': 40.7527, 'longitude': -73.9772, 'accessible': True, 'borough': 'Manhattan'},
        {'id': '635', 'name': 'Union Square-14 St', 'latitude': 40.7347, 'longitude': -73.9897, 'accessible': True, 'borough': 'Manhattan'},
        {'id': 'D24', 'name': 'Atlantic Av-Barclays Ctr', 'latitude': 40.6847, 'longitude': -73.9777, 'accessible': True, 'borough': 'Brooklyn'},
        {'id': 'R11', 'name': '34 St-Penn Station', 'latitude': 40.7505, 'longitude': -73.9935, 'accessible': True, 'borough': 'Manhattan'},
        {'id': '725', 'name': '74 St-Broadway', 'latitude': 40.7462, 'longitude': -73.8917, 'accessible': True, 'borough': 'Queens'},
        {'id': 'A42', 'name': 'Jay St-MetroTech', 'latitude': 40.6925, 'longitude': -73.9865, 'accessible': True, 'borough': 'Brooklyn'},
        {'id': '101', 'name': 'South Ferry', 'latitude': 40.7018, 'longitude': -74.0137, 'accessible': True, 'borough': 'Manhattan'},
        {'id': 'D43', 'name': 'Prospect Park', 'latitude': 40.6615, 'longitude': -73.9618, 'accessible': False, 'borough': 'Brooklyn'},
        {'id': '621', 'name': '125 St', 'latitude': 40.8075, 'longitude': -73.9386, 'accessible': True, 'borough': 'Manhattan'},
    ]
    
    for station_data in stations_data:
        station = Station(**station_data)
        db.session.add(station)
    
    db.session.commit()
    print("✓ Initial data seeded successfully")