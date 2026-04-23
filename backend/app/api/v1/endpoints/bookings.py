from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.services.booking_service import create_booking, get_user_bookings, update_booking_status
from pydantic import BaseModel
from datetime import datetime
from typing import List

router = APIRouter(prefix="/bookings", tags=["Bookings"])

class BookingRequest(BaseModel):
    mentor_id: int
    start_time: datetime
    end_time: datetime

@router.post("/")
def book_session(data: BookingRequest, db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        return create_booking(db, int(user["sub"]), data.mentor_id, data.start_time, data.end_time)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my")
def my_bookings(role: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    return get_user_bookings(db, int(user["sub"]), role)

@router.patch("/{booking_id}")
def change_status(booking_id: int, status: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    # Simple security: ideally verify if user is the mentor for this session
    return update_booking_status(db, booking_id, status)
