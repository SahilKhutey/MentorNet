from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
from fastapi import Request, HTTPException
from app.core.cache import cache_manager

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a plain text password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against a hashed version."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Generate a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(user_id: str) -> str:
    """Generate a long-lived refresh token."""
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode = {"exp": expire, "sub": str(user_id), "type": "refresh"}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def blacklist_token(token: str, expires_in: int):
    """Add a token to the Redis blacklist."""
    key = f"blacklist:{token}"
    cache_manager.set(key, "1", expire=expires_in)

def is_token_blacklisted(token: str) -> bool:
    """Check if a token has been invalidated."""
    if not cache_manager.enabled:
        return False
    return cache_manager.get(f"blacklist:{token}") is not None

# Advanced Production Rate Limiting
async def rate_limit_middleware(request: Request, call_next):
    if not cache_manager.enabled:
        return await call_next(request)

    path = request.url.path
    client_ip = request.client.host
    
    # Define limits based on operation type
    limit = 100 # Default
    window = 60 # 1 minute
    
    # Standardize path for matching
    if "auth" in path:
        limit = 5
    elif "booking" in path:
        limit = 10
    elif "search" in path or "recommendations" in path:
        limit = 20
    elif path == "/" or "health" in path:
        return await call_next(request)
    else:
        limit = 50 # General API limit

    key = f"rate_limit:{client_ip}:{path}"
    
    try:
        current_count = cache_manager.get(key) or 0
        if int(current_count) >= limit:
            raise HTTPException(
                status_code=429, 
                detail=f"Rate limit exceeded. Max {limit} requests per minute for this operation."
            )

        if int(current_count) == 0:
            cache_manager.set(key, 1, expire=window)
        else:
            cache_manager.set(key, int(current_count) + 1, expire=window)
    except HTTPException:
        raise
    except Exception as e:
        # Fail open if Redis is down, but log the error
        print(f"Rate limit error: {e}")
        pass

    return await call_next(request)
