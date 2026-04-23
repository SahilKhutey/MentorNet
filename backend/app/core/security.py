from fastapi import Request, HTTPException
from app.core.cache import cache_manager
import time

async def rate_limit_middleware(request: Request, call_next):
    # Only rate limit API requests
    if not request.url.path.startswith("/api/v1/search") and \
       not request.url.path.startswith("/api/v1/recommendations"):
        return await call_next(request)

    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"
    
    if not cache_manager.enabled:
        return await call_next(request)

    # 10 requests per minute limit
    limit = 10
    window = 60
    
    current_count = cache_manager.get(key) or 0
    if int(current_count) >= limit:
        raise HTTPException(status_code=429, detail="Too many AI requests. Please wait a minute.")

    # Increment and set expiry if new
    if int(current_count) == 0:
        cache_manager.set(key, 1, expire=window)
    else:
        # Note: Ideally use redis.incr() directly for atomicity
        cache_manager.set(key, int(current_count) + 1, expire=window)

    return await call_next(request)
