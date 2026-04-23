from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.schemas.auth_schema import SignupRequest, LoginRequest, TokenResponse
from app.services.auth_service import signup_user, login_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=TokenResponse)
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    try:
        token = signup_user(db, data.email, data.password, data.role)
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        token = login_user(db, data.email, data.password)
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
