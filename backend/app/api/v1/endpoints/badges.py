from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.dependencies import get_db, get_current_user
from app.models.badge import Badge
from app.models.user import User

router = APIRouter(prefix="/badges", tags=["Badges"])

@router.get("/")
def list_available_badges(db: Session = Depends(get_db)):
    """
    Returns all badges available in the system.
    """
    return db.query(Badge).all()

@router.get("/my")
def get_my_badges(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Returns badges earned by the current user.
    """
    user_obj = db.query(User).filter(User.id == str(user["sub"])).first()
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user_obj.badges

@router.get("/user/{user_id}")
def get_user_badges(user_id: str, db: Session = Depends(get_db)):
    """
    Public endpoint to view badges of a specific user/mentor.
    """
    user_obj = db.query(User).filter(User.id == user_id).first()
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user_obj.badges
