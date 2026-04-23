from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
import uuid

def signup_user(db: Session, email: str, password: str, role: str):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise Exception("User already exists")
    
    user = User(
        email=email,
        hashed_password=hash_password(password),
        role=role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    token = create_access_token({"sub": str(user.id), "role": user.role.value if hasattr(user.role, 'value') else user.role})
    return token

def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise Exception("Invalid credentials")
    
    token = create_access_token({"sub": str(user.id), "role": user.role.value if hasattr(user.role, 'value') else user.role})
    return token
