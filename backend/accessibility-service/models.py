from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Elevator(db.Model):
    __tablename__ = 'elevators'
    
    id = db.Column(db.String(50), primary_key=True)
    station_id = db.Column(db.String(10), nullable=False, index=True)
    status = db.Column(db.String(20), default='active')  # active, outage, maintenance
    location_description = db.Column(db.String(200))
    ada_compliance = db.Column(db.Boolean, default=True)
    outage_start = db.Column(db.DateTime, nullable=True)
    outage_end = db.Column(db.DateTime, nullable=True)
    estimated_repair = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'station_id': self.station_id,
            'status': self.status,
            'location_description': self.location_description,
            'ada_compliance': self.ada_compliance,
            'outage_start': self.outage_start.isoformat() if self.outage_start else None,
            'outage_end': self.outage_end.isoformat() if self.outage_end else None,
            'estimated_repair': self.estimated_repair.isoformat() if self.estimated_repair else None,
            'updated_at': self.updated_at.isoformat()
        }


class Escalator(db.Model):
    __tablename__ = 'escalators'
    
    id = db.Column(db.String(50), primary_key=True)
    station_id = db.Column(db.String(10), nullable=False, index=True)
    status = db.Column(db.String(20), default='active')
    location_description = db.Column(db.String(200))
    direction = db.Column(db.String(20))  # up, down, bidirectional
    outage_start = db.Column(db.DateTime, nullable=True)
    outage_end = db.Column(db.DateTime, nullable=True)
    estimated_repair = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'station_id': self.station_id,
            'status': self.status,
            'location_description': self.location_description,
            'direction': self.direction,
            'outage_start': self.outage_start.isoformat() if self.outage_start else None,
            'outage_end': self.outage_end.isoformat() if self.outage_end else None,
            'estimated_repair': self.estimated_repair.isoformat() if self.estimated_repair else None,
            'updated_at': self.updated_at.isoformat()
        }


class StationAccessibility(db.Model):
    __tablename__ = 'station_accessibility'
    
    station_id = db.Column(db.String(10), primary_key=True)
    station_name = db.Column(db.String(100), nullable=False)
    ada_compliant = db.Column(db.Boolean, default=False)
    has_elevator = db.Column(db.Boolean, default=False)
    elevator_count = db.Column(db.Integer, default=0)
    has_escalator = db.Column(db.Boolean, default=False)
    escalator_count = db.Column(db.Integer, default=0)
    accessibility_notes = db.Column(db.Text)
    reliability_score = db.Column(db.Float, default=100.0)  # 0-100 based on uptime
    last_verified = db.Column(db.DateTime, default=datetime.utcnow)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    def to_dict(self, include_equipment=False):
        data = {
            'station_id': self.station_id,
            'station_name': self.station_name,
            'ada_compliant': self.ada_compliant,
            'has_elevator': self.has_elevator,
            'elevator_count': self.elevator_count,
            'has_escalator': self.has_escalator,
            'escalator_count': self.escalator_count,
            'accessibility_notes': self.accessibility_notes,
            'reliability_score': round(self.reliability_score, 2),
            'last_verified': self.last_verified.isoformat(),
            'coordinates': {
                'latitude': self.latitude,
                'longitude': self.longitude
            } if self.latitude and self.longitude else None
        }
        
        if include_equipment:
            elevators = Elevator.query.filter_by(station_id=self.station_id).all()
            escalators = Escalator.query.filter_by(station_id=self.station_id).all()
            data['elevators'] = [e.to_dict() for e in elevators]
            data['escalators'] = [e.to_dict() for e in escalators]
            data['working_elevators'] = len([e for e in elevators if e.status == 'active'])
            data['working_escalators'] = len([e for e in escalators if e.status == 'active'])
        
        return data

