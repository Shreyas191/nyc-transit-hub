"""
In-memory cache manager for equipment and station data
No database required - everything stored in memory
"""
from datetime import datetime, timedelta
import threading

class CacheManager:
    def __init__(self, ttl=300):
        self.ttl = ttl  # Time to live in seconds
        self.cache = {}
        self.lock = threading.Lock()
    
    def get(self, key):
        """Get value from cache if not expired"""
        with self.lock:
            if key in self.cache:
                entry = self.cache[key]
                if datetime.utcnow() < entry['expires_at']:
                    return entry['data']
                else:
                    # Remove expired entry
                    del self.cache[key]
            return None
    
    def set(self, key, data, ttl=None):
        """Set value in cache with expiration"""
        cache_ttl = ttl if ttl is not None else self.ttl
        with self.lock:
            self.cache[key] = {
                'data': data,
                'expires_at': datetime.utcnow() + timedelta(seconds=cache_ttl),
                'cached_at': datetime.utcnow()
            }
    
    def delete(self, key):
        """Delete value from cache"""
        with self.lock:
            if key in self.cache:
                del self.cache[key]
    
    def clear(self):
        """Clear all cache"""
        with self.lock:
            self.cache.clear()
    
    def get_all_keys(self):
        """Get all cache keys"""
        with self.lock:
            return list(self.cache.keys())


# Global cache instance
cache = CacheManager(ttl=300)