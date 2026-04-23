from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
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
        profile = profile_service.create_profile(db, int(user["sub"]), data)
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
        profile = profile_service.update_profile(db, int(user["sub"]), data)
        return profile
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/me", response_model=ProfileResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    profile = profile_service.get_my_profile(db, int(user["sub"]))
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
