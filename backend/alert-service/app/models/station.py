from app import db
from datetime import datetime

class Station(db.Model):
    __tablename__ = 'stations'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    accessible = db.Column(db.Boolean, default=False)
    borough = db.Column(db.String(50))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'accessible': self.accessible,
            'borough': self.borough,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
