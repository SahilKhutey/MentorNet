from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.schemas.booking_schema import CreateBooking, BookingResponse, AvailabilityCreate, AvailabilityResponse
from app.services.booking_service import create_booking, add_availability, get_user_bookings
from typing import List

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", response_model=BookingResponse)
def book_session(
    data: CreateBooking,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    try:
        return create_booking(db, user_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/availability", response_model=AvailabilityResponse)
def set_availability(
    data: AvailabilityCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    # In a real app, verify user is a mentor
    return add_availability(db, user_id, data)

@router.get("/my", response_model=List[BookingResponse])
def get_my_bookings(
    is_mentor: bool = False,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    return get_user_bookings(db, user_id, is_mentor)
