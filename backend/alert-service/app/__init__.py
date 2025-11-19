from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Register blueprints
    from app.routes.routes import routes_bp
    from app.routes.stations import stations_bp
    from app.routes.realtime import realtime_bp
    from app.routes.status import status_bp
    from app.routes.alerts import alerts_bp  # NEW
    
    app.register_blueprint(routes_bp, url_prefix='/api/routes')
    app.register_blueprint(stations_bp, url_prefix='/api/stations')
    app.register_blueprint(realtime_bp, url_prefix='/api/realtime')
    app.register_blueprint(status_bp, url_prefix='/api/status')
    app.register_blueprint(alerts_bp, url_prefix='/api/alerts')  # NEW
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Start background scheduler
    from app.services.mta_api_service import start_scheduler
    start_scheduler(app)
    
    return app