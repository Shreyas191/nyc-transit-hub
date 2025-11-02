from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firebase_uid = db.Column(db.String(128), index=True, nullable=False)
    item_type = db.Column(db.String(20), nullable=False)  # 'station' or 'route'
    item_id = db.Column(db.String(50), nullable=False)    # stop_id or route_id
    item_name = db.Column(db.String(100), nullable=False)
    route_id = db.Column(db.String(50))
    custom_note = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)