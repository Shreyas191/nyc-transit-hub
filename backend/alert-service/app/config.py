import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Get absolute path to the service directory
BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / 'instance'

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-transit')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        f'sqlite:///{INSTANCE_DIR}/alerts.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # MTA API Configuration
    MTA_API_BASE_URL = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds'
    
    # Cache Configuration
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    CACHE_DEFAULT_TIMEOUT = 60  # seconds
    
    # Update intervals (in seconds)
    REALTIME_UPDATE_INTERVAL = 30
    STATUS_UPDATE_INTERVAL = 60