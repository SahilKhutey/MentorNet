import redis
import json
from app.core.config import settings
from typing import Any, Optional

class CacheManager:
    def __init__(self):
        try:
            self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
            self.redis.ping()
            self.enabled = True
        except Exception:
            print("Warning: Redis not available. Caching disabled.")
            self.enabled = False

    def get(self, key: str) -> Optional[Any]:
        if not self.enabled: return None
        data = self.redis.get(key)
        return json.loads(data) if data else None

    def set(self, key: str, value: Any, expire: int = 3600):
        if not self.enabled: return
        self.redis.set(key, json.dumps(value), ex=expire)

    def delete(self, key: str):
        if not self.enabled: return
        self.redis.delete(key)

    def cached(self, expire: int = 3600):
        """Decorator to cache function results in Redis."""
        import functools
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if not self.enabled:
                    return func(*args, **kwargs)
                
                # Create a stable key from function name and args
                key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
                cached_val = self.get(key)
                if cached_val:
                    return cached_val
                
                result = func(*args, **kwargs)
                self.set(key, result, expire=expire)
                return result
            return wrapper
        return decorator

cache_manager = CacheManager()
