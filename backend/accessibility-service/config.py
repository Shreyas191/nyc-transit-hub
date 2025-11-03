"""
Configuration settings for Accessibility Service
"""
import os

class Config:
    # Service settings
    SERVICE_NAME = 'Accessibility Service'
    SERVICE_PORT = 8005
    
    # Real MTA API Endpoints (No API key required)
    MTA_EQUIPMENT_API = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fnyct_ene.json'
    MTA_STATIONS_CSV = 'http://web.mta.info/developers/data/nyct/subway/Stations.csv'
    
    # Cache settings (in-memory, no database)
    CACHE_TTL = 300  # 5 minutes cache
    EQUIPMENT_UPDATE_INTERVAL = 600  # 10 minutes sync
    
    # Route planning
    MAX_TRANSFER_DISTANCE_KM = 0.5