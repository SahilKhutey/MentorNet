from sqlalchemy.orm import Session
from app.models.user import User, RefreshToken
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from datetime import datetime, timedelta

def signup_user(db: Session, data):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise Exception("User already exists")
    
    user = User(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        role=data.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    access_token = create_access_token({"sub": str(user.id), "role": user.role})
    refresh_token_str = create_refresh_token(user.id)
    
    # Store refresh token in DB
    db_refresh = RefreshToken(
        user_id=user.id,
        token=refresh_token_str,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )
    db.add(db_refresh)
    db.commit()
    
    return access_token, refresh_token_str

def login_user(db: Session, data):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise Exception("Invalid credentials")
    
    access_token = create_access_token({"sub": str(user.id), "role": user.role})
    refresh_token_str = create_refresh_token(user.id)
    
    # Store/Update refresh token
    # For security, we should revoke old ones, but for now we just add a new one
    db_refresh = RefreshToken(
        user_id=user.id,
        token=refresh_token_str,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )
    db.add(db_refresh)
    db.commit()
    
    return access_token, refresh_token_str

def refresh_access_token(db: Session, refresh_token: str):
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token,
        RefreshToken.revoked == None,
        RefreshToken.expires_at > datetime.utcnow()
    ).first()
    
    if not db_token:
        raise Exception("Invalid or expired refresh token")
    
    user = db.query(User).filter(User.id == db_token.user_id).first()
    if not user:
        raise Exception("User not found")
        
    # Rotate: Revoke old, issue new
    db_token.revoked = datetime.utcnow()
    
    new_access = create_access_token({"sub": str(user.id), "role": user.role})
    new_refresh = create_refresh_token(user.id)
    
    db_new_refresh = RefreshToken(
        user_id=user.id,
        token=new_refresh,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )
    db.add(db_new_refresh)
    db.commit()
    
    return new_access, new_refresh
