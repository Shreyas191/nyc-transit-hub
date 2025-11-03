"""
Reliability calculation service
Calculates uptime percentages for equipment and stations
"""
from datetime import datetime, timedelta
from models import db, Elevator, Escalator, StationAccessibility
from sqlalchemy import func

class ReliabilityService:
    def __init__(self, lookback_days=30):
        self.lookback_days = lookback_days
        
    def calculate_reliability_scores(self):
        """
        Calculate reliability scores for all stations based on equipment uptime
        """
        print(f"[{datetime.utcnow()}] Calculating reliability scores...")
        
        try:
            stations = StationAccessibility.query.all()
            cutoff_date = datetime.utcnow() - timedelta(days=self.lookback_days)
            
            for station in stations:
                # Get all elevators for this station
                elevators = Elevator.query.filter_by(station_id=station.station_id).all()
                
                if not elevators:
                    station.reliability_score = 100.0
                    continue
                
                total_score = 0
                for elevator in elevators:
                    # Calculate uptime based on outage history
                    # Simplified: if currently in outage, reduce score
                    if elevator.status == 'outage':
                        # Calculate how long it's been out
                        if elevator.outage_start:
                            outage_hours = (datetime.utcnow() - elevator.outage_start).total_seconds() / 3600
                            penalty = min(outage_hours * 2, 50)  # Max 50% penalty
                            total_score += (100 - penalty)
                        else:
                            total_score += 70  # Default penalty for unknown outage duration
                    else:
                        total_score += 100
                
                # Average score across all elevators
                station.reliability_score = total_score / len(elevators) if elevators else 100.0
                station.last_verified = datetime.utcnow()
            
            db.session.commit()
            print(f"[{datetime.utcnow()}] Reliability scores calculated successfully")
            return True
            
        except Exception as e:
            print(f"Error calculating reliability scores: {str(e)}")
            db.session.rollback()
            return False
