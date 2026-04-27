from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.models.availability import Availability
from app.services.meeting_service import meeting_service
from datetime import datetime, timedelta
import uuid

class BookingService:
    @staticmethod
    async def create_booking(db: Session, student_id: str, mentor_id: str, slot_id: str, topic: str, notes: str):
        # Prevent self-booking exploit
        if student_id == mentor_id:
            raise Exception("Security Error: You cannot book a session with yourself.")

        # Atomic Update to claim the slot (Prevents Race Conditions)
        result = db.query(Availability).filter(
            Availability.id == slot_id,
            Availability.mentor_id == mentor_id,
            Availability.is_booked == False,
            Availability.start_time > datetime.now()
        ).update({"is_booked": True}, synchronize_session=False)

        if result == 0:
             raise Exception("Availability slot not found, already booked, or in the past.")
        
        # Now get the slot data to create the booking record
        slot = db.query(Availability).filter(Availability.id == slot_id).first()
        
        # Create booking
        booking_id = str(uuid.uuid4())
        # Generate secure meeting link
        meeting_link = meeting_service.generate_room_link(booking_id)

        booking = Booking(
            id=booking_id,
            student_id=student_id,
            mentor_id=mentor_id,
            start_time=slot.start_time,
            end_time=slot.end_time,
            topic=topic,
            notes=notes,
            meeting_link=meeting_link,
            status="confirmed"
        )
        db.add(booking)
        
        db.commit()
        db.refresh(booking)

        # 3. Trigger Notifications (Real-time)
        from app.services.notification_service import notification_service
        # Use a separate background task or await here since we are in an async context
        # Note: We need to ensure create_booking is called with 'await'
        await notification_service.create_notification(
            db,
            user_id=mentor_id,
            title="New Mentorship Booking",
            message=f"A student has booked a session: {topic}",
            type="booking"
        )
        
        return booking

    @staticmethod
    def get_user_bookings(db: Session, user_id: str, role: str):
        if role == "mentor":
            return db.query(Booking).filter(Booking.mentor_id == user_id).all()
        else:
            return db.query(Booking).filter(Booking.student_id == user_id).all()

    @staticmethod
    def update_booking_status(db: Session, booking_id: str, status: str):
        db.query(Booking).filter(Booking.id == booking_id).update({"status": status})
        db.commit()
        return {"status": "updated"}

booking_service = BookingService()
