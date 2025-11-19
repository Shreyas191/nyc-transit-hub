import json
import redis
from flask import current_app

class CacheService:
    _redis_client = None
    
    @classmethod
    def get_redis(cls):
        if cls._redis_client is None:
            try:
                cls._redis_client = redis.from_url(
                    current_app.config['REDIS_URL'],
                    decode_responses=True
                )
            except Exception as e:
                print(f"Redis connection failed: {e}")
                return None
        return cls._redis_client
    
    @classmethod
    def get(cls, key):
        client = cls.get_redis()
        if not client:
            return None
        
        try:
            value = client.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None
    
    @classmethod
    def set(cls, key, value, timeout=None):
        client = cls.get_redis()
        if not client:
            return False
        
        try:
            timeout = timeout or current_app.config['CACHE_DEFAULT_TIMEOUT']
            client.setex(key, timeout, json.dumps(value, default=str))
            return True
        except Exception as e:
            print(f"Cache set error: {e}")
            return False