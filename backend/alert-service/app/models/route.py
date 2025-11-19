from app import db
from datetime import datetime

class Route(db.Model):
    __tablename__ = 'routes'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50))  # subway, bus, rail
    color = db.Column(db.String(7))  # Hex color
    text_color = db.Column(db.String(7))  # Text color for contrast
    description = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    service_statuses = db.relationship('ServiceStatus', backref='route', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'color': self.color,
            'text_color': self.text_color,
            'description': self.description,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }