from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.dependencies import get_db, require_role
from app.services.scheduling_service import (
    set_availability, 
    get_available_slots, 
    book_slot, 
    update_booking_status
)

router = APIRouter(prefix="/schedule", tags=["Scheduling"])

@router.post("/availability")
def add_availability(
    slots: List[dict],
    db: Session = Depends(get_db),
    user=Depends(require_role("mentor"))
):
    """
    Mentor endpoint to define open time slots for bookings.
    """
    try:
        set_availability(db, str(user["sub"]), slots)
        return {"status": "availability slots added"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/availability/{mentor_id}")
def view_slots(mentor_id: int, db: Session = Depends(get_db)):
    """
    Public/Student endpoint to see a mentor's bookable slots.
    """
    return get_available_slots(db, mentor_id)

@router.post("/book")
def book(
    mentor_id: int,
    start: str,
    end: str,
    db: Session = Depends(get_db),
    user=Depends(require_role("student"))
):
    """
    Student endpoint to book a specific mentor slot.
    """
    try:
        booking = book_slot(db, str(user["sub"]), mentor_id, start, end)
        return {"booking_id": booking.id, "status": booking.status}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/status")
def update_status(
    booking_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    """
    Transition the session status (e.g., mark as completed).
    """
    try:
        update_booking_status(db, booking_id, status)
        return {"updated": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
