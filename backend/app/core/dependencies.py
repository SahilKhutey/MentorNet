from typing import Generator
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.core.database import SessionLocal
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_role(required_role: str):
    def role_checker(user=Depends(get_current_user)):
        if user.get("role") != required_role:
            raise HTTPException(status_code=403, detail="Access denied")
        return user
    return role_checker
