from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from .config import Config
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Create instance directory if it doesn't exist
    instance_path = os.path.join(os.path.dirname(__file__), '..', 'instance')
    os.makedirs(instance_path, exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Register blueprints
    from app.routes.routes import routes_bp
    from app.routes.stations import stations_bp
    from app.routes.realtime import realtime_bp
    from app.routes.trips import trips_bp
    
    app.register_blueprint(routes_bp, url_prefix='/api/routes')
    app.register_blueprint(stations_bp, url_prefix='/api/stations')
    app.register_blueprint(realtime_bp, url_prefix='/api/realtime')
    app.register_blueprint(trips_bp, url_prefix='/api/trips')
    
    # Health check
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'service': 'transit-service'}, 200
    
    # Create tables
    with app.app_context():
        db.create_all()
        
        # Seed initial data if database is empty
        from app.services.seed_service import seed_initial_data
        seed_initial_data()
    
    # Start background scheduler
    from app.services.scheduler import start_scheduler
    start_scheduler(app)
    
    return app
