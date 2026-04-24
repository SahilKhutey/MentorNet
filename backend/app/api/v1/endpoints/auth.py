from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, security
from app.schemas.auth_schema import SignupRequest, LoginRequest, AuthResponse, RefreshRequest
from app.services.auth_service import signup_user, login_user, refresh_access_token
from app.core.security import blacklist_token
from jose import jwt
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])

from fastapi import APIRouter, Depends, HTTPException, status, Request, Response

@router.post("/signup", response_model=AuthResponse)
def signup(data: SignupRequest, response: Response, db: Session = Depends(get_db)):
    try:
        access, refresh = signup_user(db, data)
        response.set_cookie(
            key="refresh_token", 
            value=refresh, 
            httponly=True, 
            secure=True, 
            samesite="strict",
            max_age=60*60*24*7 # 7 days
        )
        return {"access_token": access, "refresh_token": "set_in_cookie", "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=AuthResponse)
def login(data: LoginRequest, response: Response, db: Session = Depends(get_db)):
    try:
        access, refresh = login_user(db, data)
        response.set_cookie(
            key="refresh_token", 
            value=refresh, 
            httponly=True, 
            secure=True, 
            samesite="strict",
            max_age=60*60*24*7
        )
        return {"access_token": access, "refresh_token": "set_in_cookie", "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/refresh", response_model=AuthResponse)
def refresh(request: Request, response: Response, db: Session = Depends(get_db)):
    try:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise Exception("No refresh token in cookies")
            
        access, new_refresh = refresh_access_token(db, refresh_token)
        response.set_cookie(
            key="refresh_token", 
            value=new_refresh, 
            httponly=True, 
            secure=True, 
            samesite="strict",
            max_age=60*60*24*7
        )
        return {"access_token": access, "refresh_token": "set_in_cookie", "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/logout")
def logout(token=Depends(security)):
    """Blacklist the current access token."""
    try:
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        exp = payload.get("exp")
        now = int(jwt.time.time())
        rem = exp - now
        if rem > 0:
            blacklist_token(token.credentials, rem)
        return {"message": "Successfully logged out"}
    except Exception:
        return {"message": "Token already invalid or expired"}
