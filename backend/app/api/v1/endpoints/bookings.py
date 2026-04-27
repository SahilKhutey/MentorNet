from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.services.booking_service import booking_service
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

router = APIRouter(prefix="/bookings", tags=["Bookings"])

class BookingRequest(BaseModel):
    mentor_id: str
    slot_id: str
    topic: str
    notes: Optional[str] = ""

@router.post("/")
async def book_session(data: BookingRequest, db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        return await booking_service.create_booking(
            db, 
            str(user["sub"]), 
            data.mentor_id, 
            data.slot_id, 
            data.topic, 
            data.notes
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my")
def my_bookings(role: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    return booking_service.get_user_bookings(db, str(user["sub"]), role)

@router.patch("/{booking_id}")
def change_status(booking_id: str, status: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    # Simple security: ideally verify if user is the mentor for this session
    return booking_service.update_booking_status(db, booking_id, status)
