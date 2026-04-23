from sqlalchemy.orm import Session
from datetime import datetime
from app.models.availability import Availability
from app.models.session import Session as MentorshipSession
from app.core.privacy import PrivacyEnforcer

def set_availability(db: Session, mentor_id: int, slots, user_role: str):
    """
    Overwrites or adds new availability slots for a mentor.
    """
    PrivacyEnforcer.verify_mentor_action(user_role)
    
    for slot in slots:
        av = Availability(
            mentor_id=mentor_id,
            start_time=datetime.fromisoformat(slot["start"]),
            end_time=datetime.fromisoformat(slot["end"])
        )
        db.add(av)
    db.commit()

def get_available_slots(db: Session, mentor_id: int):
    """
    Retrieves availability slots that aren't already booked or pending.
    """
    slots = db.query(Availability).filter(
        Availability.mentor_id == mentor_id
    ).all()
    
    # Fetch active bookings that might conflict
    bookings = db.query(MentorshipSession).filter(
        MentorshipSession.mentor_id == mentor_id,
        MentorshipSession.status.in_(["pending", "confirmed"])
    ).all()
    
    booked_times = [(b.start_time, b.end_time) for b in bookings]
    
    available = []
    for s in slots:
        overlap = False
        for b_start, b_end in booked_times:
            # Overlap check logic
            if not (s.end_time <= b_start or s.start_time >= b_end):
                overlap = True
                break
        if not overlap:
            available.append(s)
            
    return available

def book_slot(db: Session, student_id: int, mentor_id: int, start: str, end: str):
    """
    Creates a new mentorship session after verifying no conflicts exist.
    """
    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)

    # Check for existing booking conflicts
    conflict = db.query(MentorshipSession).filter(
        MentorshipSession.mentor_id == mentor_id,
        MentorshipSession.start_time < end_dt,
        MentorshipSession.end_time > start_dt,
        MentorshipSession.status.in_(["pending", "confirmed"])
    ).first()

    if conflict:
        raise Exception("This slot is already booked or pending.")

    booking = MentorshipSession(
        student_id=student_id,
        mentor_id=mentor_id,
        start_time=start_dt,
        end_time=end_dt,
        status="confirmed" # Or pending if approval is needed
    )
    
    db.add(booking)
    db.commit()
    db.refresh(booking)
    
    return booking

def update_booking_status(db: Session, booking_id: int, status: str):
    """
    Transition session through its lifecycle (confirmed -> completed).
    """
    booking = db.query(MentorshipSession).filter(MentorshipSession.id == booking_id).first()
    if not booking:
        raise Exception("Booking not found")
    
    booking.status = status
    db.commit()
    db.refresh(booking)
    
    return booking
