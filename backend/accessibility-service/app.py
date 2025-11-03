"""
Main application entry point
Accessibility Service - Port 8005
"""
from flask import Flask, jsonify
from config import Config
from routes.stations import stations_bp
from routes.equipment import equipment_bp
from routes.routes import routes_bp
from services.mta_client import mta_client
from services.cache_manager import cache
import threading
import time
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Register blueprints
app.register_blueprint(stations_bp)
app.register_blueprint(equipment_bp)
app.register_blueprint(routes_bp)

def update_equipment_job():
    """Background job to update equipment status from MTA"""
    print(f"[{datetime.utcnow()}] Starting equipment update background job")
    
    with app.app_context():
        mta_client.fetch_equipment_status()
        mta_client.fetch_stations()
    
    while True:
        time.sleep(Config.EQUIPMENT_UPDATE_INTERVAL)
        with app.app_context():
            mta_client.fetch_equipment_status()

@app.route('/')
def index():
    """Service health check and information"""
    equipment = cache.get('equipment_data')
    stations = cache.get('stations_data')
    
    return jsonify({
        'service': Config.SERVICE_NAME,
        'status': 'running',
        'port': Config.SERVICE_PORT,
        'version': '1.0.0',
        'data_source': 'Real-time MTA APIs',
        'cache_status': {
            'equipment_cached': equipment is not None,
            'stations_cached': stations is not None,
            'last_equipment_update': equipment.get('last_updated') if equipment else None,
            'total_elevators': equipment.get('total_elevators', 0) if equipment else 0,
            'total_escalators': equipment.get('total_escalators', 0) if equipment else 0,
            'total_stations': len(stations) if stations else 0
        },
        'endpoints': {
            'stations': '/api/accessibility/stations',
            'elevators': '/api/accessibility/elevators',
            'escalators': '/api/accessibility/escalators',
            'outages': '/api/accessibility/elevators/outages',
            'route': '/api/accessibility/route?origin=X&destination=Y',
            'alternatives': '/api/accessibility/alternatives/{station_id}'
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    equipment = cache.get('equipment_data')
    stations = cache.get('stations_data')
    is_healthy = equipment is not None and stations is not None
    
    return jsonify({
        'status': 'healthy' if is_healthy else 'degraded',
        'timestamp': datetime.utcnow().isoformat(),
        'checks': {
            'equipment_data': 'ok' if equipment else 'missing',
            'stations_data': 'ok' if stations else 'missing',
            'cache_operational': 'ok'
        }
    }), 200 if is_healthy else 503

@app.route('/api/accessibility/refresh', methods=['POST'])
def refresh_data():
    """Manually trigger data refresh from MTA"""
    try:
        equipment = mta_client.fetch_equipment_status()
        stations = mta_client.fetch_stations()
        return jsonify({
            'status': 'success',
            'message': 'Data refreshed successfully',
            'data': {
                'elevators': equipment.get('total_elevators', 0),
                'escalators': equipment.get('total_escalators', 0),
                'stations': len(stations),
                'last_updated': equipment.get('last_updated')
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Failed to refresh: {str(e)}'}), 500

@app.route('/api/accessibility/stats', methods=['GET'])
def get_stats():
    """Get system-wide accessibility statistics"""
    equipment = cache.get('equipment_data')
    if not equipment:
        equipment = mta_client.fetch_equipment_status()
    
    stations = cache.get('stations_data')
    if not stations:
        stations = mta_client.fetch_stations()
    
    total_elevators = len(equipment.get('elevators', []))
    active_elevators = len([e for e in equipment.get('elevators', []) if e['status'] == 'active'])
    outage_elevators = len([e for e in equipment.get('elevators', []) if e['status'] == 'outage'])
    
    total_escalators = len(equipment.get('escalators', []))
    active_escalators = len([e for e in equipment.get('escalators', []) if e['status'] == 'active'])
    
    ada_stations = len([s for s in stations if s.get('ada_compliant')])
    elevator_uptime = (active_elevators / total_elevators * 100) if total_elevators > 0 else 0
    
    return jsonify({
        'status': 'success',
        'data': {
            'system_wide': {
                'total_stations': len(stations),
                'ada_compliant_stations': ada_stations,
                'ada_compliance_rate': round(ada_stations / len(stations) * 100, 2) if stations else 0
            },
            'elevators': {
                'total': total_elevators,
                'active': active_elevators,
                'outage': outage_elevators,
                'uptime_percentage': round(elevator_uptime, 2)
            },
            'escalators': {
                'total': total_escalators,
                'active': active_escalators
            },
            'last_updated': equipment.get('last_updated')
        }
    })

if __name__ == '__main__':
    print(f"\n{'='*60}")
    print(f"🚇 {Config.SERVICE_NAME} Starting")
    print(f"{'='*60}")
    print(f"Port: {Config.SERVICE_PORT}")
    print(f"Data Source: Real-time MTA APIs")
    print(f"Cache TTL: {Config.CACHE_TTL}s")
    print(f"Update Interval: {Config.EQUIPMENT_UPDATE_INTERVAL}s")
    print(f"No Database Required - All data in memory")
    print(f"{'='*60}\n")
    
    # Initial data fetch
    print("Performing initial data fetch from MTA...")
    try:
        equipment = mta_client.fetch_equipment_status()
        print(f"✓ Equipment data loaded: {equipment.get('total_elevators', 0)} elevators, {equipment.get('total_escalators', 0)} escalators")
        
        stations = mta_client.fetch_stations()
        print(f"✓ Stations data loaded: {len(stations)} stations")
    except Exception as e:
        print(f"⚠ Warning: Initial data fetch failed: {str(e)}")
        print("Service will continue and retry in background...")
    
    # Start background update job
    update_thread = threading.Thread(target=update_equipment_job, daemon=True)
    update_thread.start()
    print("✓ Background update job started")
    
    print(f"\n{'='*60}")
    print(f"Service ready at http://0.0.0.0:{Config.SERVICE_PORT}")
    print(f"{'='*60}\n")
    
    # Run application
    app.run(host='0.0.0.0', port=Config.SERVICE_PORT, debug=True, use_reloader=False)

