"""
MTA API synchronization service
Fetches equipment status from MTA feeds
"""
import requests
import random
from datetime import datetime, timedelta
from models import db, Elevator, Escalator, StationAccessibility

class MTASyncService:
    def __init__(self, api_key=None):
        self.api_key = api_key
        
    def sync_equipment_status(self):
        """
        Fetch latest equipment status from MTA API
        In production, this would call real MTA API
        For demo, we simulate status changes
        """
        print(f"[{datetime.utcnow()}] Syncing equipment status...")
        
        try:
            # Simulate equipment status changes
            elevators = Elevator.query.all()
            escalators = Escalator.query.all()
            
            for elevator in elevators:
                # 5% chance of status change
                if random.random() < 0.05:
                    if elevator.status == 'active':
                        # Create outage
                        elevator.status = 'outage'
                        elevator.outage_start = datetime.utcnow()
                        elevator.estimated_repair = datetime.utcnow() + timedelta(hours=random.randint(2, 48))
                    elif elevator.status == 'outage':
                        # Restore service
                        elevator.status = 'active'
                        elevator.outage_end = datetime.utcnow()
                        elevator.estimated_repair = None
                
                elevator.updated_at = datetime.utcnow()
            
            for escalator in escalators:
                # 3% chance of status change
                if random.random() < 0.03:
                    if escalator.status == 'active':
                        escalator.status = 'outage'
                        escalator.outage_start = datetime.utcnow()
                        escalator.estimated_repair = datetime.utcnow() + timedelta(hours=random.randint(1, 24))
                    elif escalator.status == 'outage':
                        escalator.status = 'active'
                        escalator.outage_end = datetime.utcnow()
                        escalator.estimated_repair = None
                
                escalator.updated_at = datetime.utcnow()
            
            db.session.commit()
            print(f"[{datetime.utcnow()}] Equipment status synced successfully")
            return True
            
        except Exception as e:
            print(f"Error syncing equipment status: {str(e)}")
            db.session.rollback()
            return False
