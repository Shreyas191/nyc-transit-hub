from flask import Flask
from config import Config
from .models import db, Favorite
from .auth import verify_token
from . import routes
from sqlalchemy import inspect, text

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('favorite')]
        if 'route_id' not in columns:
            db.session.execute(text('ALTER TABLE favorite ADD COLUMN route_id TEXT'))
            db.session.commit()

        routes.register_routes(app, db, Favorite, verify_token)

    return app