from sqlalchemy.orm import Session as DBSession
from app.models.booking import Booking
from app.models.availability import Availability
from app.models.session import Session
from app.services.socket_manager import socket_manager
import uuid

def generate_meeting_link():
    """Generate a unique Jitsi meeting link."""
    return f"https://meet.jit.si/mentornet-{uuid.uuid4()}"

def create_booking(db: DBSession, student_id: str, data):
    """Create a new session booking after validating availability and detecting conflicts."""
    
    # 1. Check if mentor has a valid availability slot for this time
    slot = db.query(Availability).filter(
        Availability.mentor_id == data.mentor_id,
        Availability.start_time <= data.start_time,
        Availability.end_time >= data.end_time
    ).first()

    if not slot:
        raise Exception("Mentor is not available at the requested time.")

    # 2. Critical Conflict Logic: Check for double bookings
    existing = db.query(Booking).filter(
        Booking.mentor_id == data.mentor_id,
        Booking.status != "cancelled",
        Booking.start_time < data.end_time,
        Booking.end_time > data.start_time
    ).first()

    if existing:
        raise Exception("Mentor already has a confirmed session at this time.")

    # 3. Create the Booking record
    booking = Booking(
        mentor_id=data.mentor_id,
        student_id=student_id,
        start_time=data.start_time,
        end_time=data.end_time,
        status="scheduled"
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    # 4. 🔥 AUTO-CREATE SESSION
    # This turns a booking into an actionable mentorship experience
    session = Session(
        booking_id=booking.id,
        mentor_id=booking.mentor_id,
        student_id=student_id,
        start_time=booking.start_time,
        end_time=booking.end_time,
        meeting_link=generate_meeting_link(),
        status="upcoming"
    )
    db.add(session)
    db.commit()

    # 5. Real-time Notification
    try:
        import asyncio
        asyncio.create_task(socket_manager.handle_booking_event(booking))
    except Exception as e:
        print(f"Failed to emit socket event: {e}")

    return booking

def add_availability(db: Session, mentor_id: str, data):
    """Mentor adds an availability window."""
    slot = Availability(
        mentor_id=mentor_id,
        start_time=data.start_time,
        end_time=data.end_time
    )
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot

def get_user_bookings(db: Session, user_id: str, is_mentor: bool = False) -> List[Booking]:
    query = db.query(Booking)
    if is_mentor:
        return query.filter(Booking.mentor_id == user_id).all()
    return query.filter(Booking.student_id == user_id).all()
