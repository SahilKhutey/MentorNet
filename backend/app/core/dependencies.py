from typing import Generator
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer
from jose import jwt
from app.core.database import SessionLocal
from app.core.config import settings
from app.core.security import is_token_blacklisted

# Security scheme
security = HTTPBearer()

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(request: Request, token=Depends(security)):
    """Extract and validate user_id from the JWT token with blacklist check."""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if is_token_blacklisted(token.credentials):
        raise HTTPException(status_code=401, detail="Token has been revoked. Please log in again.")

    try:
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub") or payload.get("user_id")
        if user_id is None:
            raise credentials_exception
            
        # Set state for audit logging
        request.state.user_id = user_id
        return user_id
    except Exception:
        raise credentials_exception

def require_role(required_role: str):
    def role_checker(user_id: str = Depends(get_current_user)):
        return user_id
    return role_checker
