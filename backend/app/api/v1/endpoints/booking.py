from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.services.booking_service import booking_service
from app.services.availability_service import availability_service
from typing import List

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/")
def book_session(
    data: dict, # Using dict for flexibility during rapid dev
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    try:
        user_id = str(user["sub"])
        return booking_service.create_booking(
            db, 
            user_id, 
            data.get("mentor_id"), 
            data.get("slot_id"), 
            data.get("topic"), 
            data.get("notes")
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/slots/{mentor_id}")
def get_mentor_slots(mentor_id: str, db: Session = Depends(get_db)):
    return availability_service.get_available_slots(db, mentor_id)

@router.get("/my")
def get_my_bookings(
    role: str = "student",
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    user_id = str(user["sub"])
    return booking_service.get_user_bookings(db, user_id, role)
