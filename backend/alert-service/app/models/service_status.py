from app import db
from datetime import datetime

class ServiceStatus(db.Model):
    __tablename__ = 'service_status'
    
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.String(50), db.ForeignKey('routes.id'), nullable=False)
    status = db.Column(db.String(50))  # good_service, delays, service_change, planned_work
    message = db.Column(db.Text)
    severity = db.Column(db.String(20))  # low, medium, high, critical
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'route_id': self.route_id,
            'status': self.status,
            'message': self.message,
            'severity': self.severity,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }