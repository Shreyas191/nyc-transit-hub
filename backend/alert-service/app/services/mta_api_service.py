import requests
from flask import current_app
from app import db
from app.models.route import Route
from app.models.station import Station
from app.models.service_status import ServiceStatus
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


class MTAAPIService:

    @staticmethod
    def fetch_service_status():
        """Fetch service status without API key (using public fallback/GTFS static feed)."""

        try:
            # Public static MTA status feed (or your own endpoint)
            url = f"{current_app.config['MTA_API_BASE_URL']}/status"

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error fetching MTA service status: {e}")
            return None

    @staticmethod
    def update_service_status():
        """Update service status in database."""
        status_data = MTAAPIService.fetch_service_status()

        if not status_data:
            return

        try:
            for route_data in status_data.get('routes', []):
                route_id = route_data.get('id')
                status = route_data.get('status', 'good_service')
                message = route_data.get('message', '')
                severity = route_data.get('severity', 'low')

                new_status = ServiceStatus(
                    route_id=route_id,
                    status=status,
                    message=message,
                    severity=severity,
                    timestamp=datetime.utcnow()
                )

                db.session.add(new_status)

            db.session.commit()
            print(f"Updated service status at {datetime.utcnow()}")

        except Exception as e:
            db.session.rollback()
            print(f"Error updating service status: {e}")

    @staticmethod
    def fetch_realtime_data(route_id):
        """Fetch realtime train positions from public GTFS-RT URL (no API key needed)."""
        try:
            url = f"{current_app.config['MTA_API_BASE_URL']}/gtfs-{route_id}"

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            return response.content  # GTFS protobuf bytes

        except requests.exceptions.RequestException as e:
            print(f"Error fetching realtime data for {route_id}: {e}")
            return None

    @staticmethod
    def seed_initial_data():
        """Seed database with initial route and station data."""
        sample_routes = [
            {'id': '1', 'name': '1', 'type': 'subway', 'color': '#EE352E', 'text_color': '#FFFFFF'},
            {'id': '2', 'name': '2', 'type': 'subway', 'color': '#EE352E', 'text_color': '#FFFFFF'},
            {'id': '3', 'name': '3', 'type': 'subway', 'color': '#EE352E', 'text_color': '#FFFFFF'},
            {'id': 'A', 'name': 'A', 'type': 'subway', 'color': '#0039A6', 'text_color': '#FFFFFF'},
            {'id': 'C', 'name': 'C', 'type': 'subway', 'color': '#0039A6', 'text_color': '#FFFFFF'},
            {'id': 'E', 'name': 'E', 'type': 'subway', 'color': '#0039A6', 'text_color': '#FFFFFF'},
            {'id': 'N', 'name': 'N', 'type': 'subway', 'color': '#FCCC0A', 'text_color': '#000000'},
            {'id': 'Q', 'name': 'Q', 'type': 'subway', 'color': '#FCCC0A', 'text_color': '#000000'},
            {'id': 'L', 'name': 'L', 'type': 'subway', 'color': '#A7A9AC', 'text_color': '#FFFFFF'},
            {'id': '7', 'name': '7', 'type': 'subway', 'color': '#B933AD', 'text_color': '#FFFFFF'},
        ]

        for route_data in sample_routes:
            if not Route.query.get(route_data['id']):
                db.session.add(Route(**route_data))

        sample_stations = [
            {'id': 'times-sq', 'name': 'Times Square-42 St', 'latitude': 40.7580, 'longitude': -73.9855, 'accessible': True, 'borough': 'Manhattan'},
            {'id': 'grand-central', 'name': 'Grand Central-42 St', 'latitude': 40.7527, 'longitude': -73.9772, 'accessible': True, 'borough': 'Manhattan'},
            {'id': 'union-sq', 'name': 'Union Square-14 St', 'latitude': 40.7347, 'longitude': -73.9897, 'accessible': True, 'borough': 'Manhattan'},
            {'id': 'atlantic-av', 'name': 'Atlantic Av-Barclays Ctr', 'latitude': 40.6847, 'longitude': -73.9777, 'accessible': True, 'borough': 'Brooklyn'},
        ]

        for station_data in sample_stations:
            if not Station.query.get(station_data['id']):
                db.session.add(Station(**station_data))

        db.session.commit()
        print("Initial data seeded successfully")


def start_scheduler(app):
    """Start background scheduler for periodic updates."""
    scheduler = BackgroundScheduler()

    def update_job():
        with app.app_context():
            MTAAPIService.update_service_status()

    scheduler.add_job(
        func=update_job,
        trigger='interval',
        seconds=app.config['STATUS_UPDATE_INTERVAL']
    )

    scheduler.start()
