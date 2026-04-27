from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.dependencies import get_db, get_current_user
from app.schemas.profile_schema import ProfileCreate, ProfileResponse, ProfileUpdate
from app.services.profile_service import profile_service

router = APIRouter(prefix="", tags=["Profile"])

@router.post("/create", response_model=ProfileResponse)
def create_user_profile(
    data: ProfileCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        profile = profile_service.create_profile(db, str(user["sub"]), data)
        return profile
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/update", response_model=ProfileResponse)
def update_user_profile(
    data: ProfileUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        profile = profile_service.update_profile(db, str(user["sub"]), data)
        return profile
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

from app.models.user import User
from sqlalchemy import func
from app.models.feedback import Feedback
from app.models.session import Session as MentorSession
from app.models.mentor import Mentor
from app.services.availability_service import availability_service

@router.post("/mentor")
def create_mentor_profile(
    data: dict,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    user_id = str(user["sub"])
    
    # Create or update mentor record
    mentor = db.query(Mentor).filter(Mentor.user_id == user_id).first()
    if not mentor:
        mentor = Mentor(user_id=user_id)
        db.add(mentor)
    
    mentor.designation = data.get("designation")
    mentor.organization = data.get("organization")
    mentor.experience_years = data.get("experience_years", 0)
    mentor.hourly_rate = data.get("hourly_rate", 0)
    
    db.commit()
    
    # Auto-generate slots for the next 7 days based on onboarding
    availability_service.generate_slots(db, user_id, datetime.utcnow(), days=7)
    
    return {"status": "success", "mentor_id": mentor.id}

@router.get("/public/{username}")
def get_public_profile(username: str, db: Session = Depends(get_db)):
    """Public endpoint for sharing mentor profiles (SEO optimized)."""
    user = db.query(User).filter(User.username == username, User.role == "mentor").first()
    if not user:
        raise HTTPException(status_code=404, detail="Mentor not found")
    
    # Aggregate Stats
    avg_rating = db.query(func.avg(Feedback.rating)).filter(Feedback.mentor_id == user.id).scalar() or 0
    total_sessions = db.query(MentorSession).filter(MentorSession.mentor_id == user.id, MentorSession.status == "completed").count()
    
    return {
        "name": user.name,
        "username": user.username,
        "bio": user.profile.bio if user.profile else "Elite Mentor",
        "institution": user.profile.institution if user.profile else "Global Network",
        "primary_field": user.profile.primary_field if user.profile else "Technology",
        "expertise": [tag.name for tag in user.profile.tags] if user.profile else [],
        "rating": round(float(avg_rating), 1),
        "session_count": total_sessions,
        "avatar": f"https://api.dicebear.com/7.x/avataaars/svg?seed={user.username}"
    }

@router.get("/me", response_model=ProfileResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    profile = profile_service.get_my_profile(db, str(user["sub"]))
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    return profile

@router.get("/search", response_model=List[ProfileResponse])
def search(
    field: Optional[str] = None,
    tags: Optional[List[str]] = Query(None),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    results = profile_service.search_profiles(db, field=field, tags=tags, skip=skip, limit=limit)
    return results

@router.get("/{user_id}", response_model=ProfileResponse)
def get_profile(
    user_id: int,
    db: Session = Depends(get_db)
):
    profile = profile_service.get_profile_by_user(db, user_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    return profile
