"""
Utility helper functions
"""
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two coordinates using Haversine formula
    Returns distance in kilometers
    """
    if not all([lat1, lon1, lat2, lon2]):
        return float('inf')
    
    R = 6371  # Earth's radius in kilometers
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    
    return distance


def format_response(data, message=None, status='success'):
    """Standardize API response format"""
    response = {
        'status': status,
        'data': data,
        'timestamp': datetime.utcnow().isoformat()
    }
    if message:
        response['message'] = message
    return response


def format_error(message, status_code=400):
    """Standardize error response format"""
    return {
        'status': 'error',
        'message': message,
        'code': status_code,
        'timestamp': datetime.utcnow().isoformat()
    }, status_code