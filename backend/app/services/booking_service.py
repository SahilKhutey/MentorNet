from sqlalchemy.orm import Session
from app.models.session import Session as MentorshipSession
from datetime import datetime
from typing import List

def create_booking(db: Session, student_id: int, mentor_id: int, start_time: datetime, end_time: datetime):
    # Check for conflicts
    existing = db.query(MentorshipSession).filter(
        MentorshipSession.mentor_id == mentor_id,
        MentorshipSession.status == "confirmed",
        MentorshipSession.start_time < end_time,
        MentorshipSession.end_time > start_time
    ).first()
    
    if existing:
        raise Exception("Mentor is already booked for this time slot")

    booking = MentorshipSession(
        student_id=student_id,
        mentor_id=mentor_id,
        start_time=start_time,
        end_time=end_time,
        status="pending"
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

def update_booking_status(db: Session, booking_id: int, status: str):
    booking = db.query(MentorshipSession).filter(MentorshipSession.id == booking_id).first()
    if not booking:
        raise Exception("Booking not found")
    
    booking.status = status
    db.commit()
    return booking

def get_user_bookings(db: Session, user_id: int, role: str) -> List[MentorshipSession]:
    if role == "mentor":
        return db.query(MentorshipSession).filter(MentorshipSession.mentor_id == user_id).all()
    else:
        return db.query(MentorshipSession).filter(MentorshipSession.student_id == user_id).all()
