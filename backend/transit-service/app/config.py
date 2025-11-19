import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Get absolute path to the service directory
BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / 'instance'

# Create instance directory if it doesn't exist
INSTANCE_DIR.mkdir(exist_ok=True)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-transit')
    
    # Use absolute path for database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        f'sqlite:///{INSTANCE_DIR}/transit.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # MTA API Configuration
    MTA_API_KEY = os.getenv('MTA_API_KEY')
    MTA_API_BASE_URL = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds'
    
    # MTA Real-Time Feed URLs (GTFS-RT)
    MTA_FEEDS = {
        # Subway feeds
        '123456S': 'nyct%2Fgtfs',  # 1,2,3,4,5,6,S trains
        'ACE': 'nyct%2Fgtfs-ace',  # A,C,E trains
        'BDFM': 'nyct%2Fgtfs-bdfm',  # B,D,F,M trains
        'G': 'nyct%2Fgtfs-g',  # G train
        'JZ': 'nyct%2Fgtfs-jz',  # J,Z trains
        'NQRW': 'nyct%2Fgtfs-nqrw',  # N,Q,R,W trains
        'L': 'nyct%2Fgtfs-l',  # L train
        '7': 'nyct%2Fgtfs-7',  # 7 train
        'SIR': 'nyct%2Fgtfs-si',  # Staten Island Railway
    }
    
    # Cache Configuration
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    CACHE_DEFAULT_TIMEOUT = 30  # seconds
    
    # Update intervals (in seconds)
    REALTIME_UPDATE_INTERVAL = 30  # Update train positions every 30 seconds
