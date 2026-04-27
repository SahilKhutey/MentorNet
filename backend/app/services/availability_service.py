from sqlalchemy.orm import Session
from app.models.availability import Availability
from datetime import datetime, timedelta
from typing import List, Dict

class AvailabilityService:
    @staticmethod
    def generate_slots(db: Session, mentor_id: str, start_date: datetime, days: int = 7):
        """
        Generates 30-minute slots for a mentor for the next N days.
        Default: 9 AM to 5 PM
        """
        slots = []
        current_date = start_date.replace(hour=9, minute=0, second=0, microsecond=0)
        
        for day in range(days):
            for hour in range(9, 17): # 9 AM to 5 PM
                for minute in [0, 30]:
                    slot_start = current_date + timedelta(days=day, hours=hour-current_date.hour, minutes=minute)
                    slot_end = slot_start + timedelta(minutes=30)
                    
                    # Check if slot already exists
                    exists = db.query(Availability).filter(
                        Availability.mentor_id == mentor_id,
                        Availability.start_time == slot_start
                    ).first()
                    
                    if not exists:
                        slot = Availability(
                            mentor_id=mentor_id,
                            start_time=slot_start,
                            end_time=slot_end
                        )
                        db.add(slot)
                        slots.append(slot)
        
        db.commit()
        return slots

    @staticmethod
    def get_available_slots(db: Session, mentor_id: str):
        return db.query(Availability).filter(
            Availability.mentor_id == mentor_id,
            Availability.start_time > datetime.utcnow()
        ).order_by(Availability.start_time.asc()).all()

availability_service = AvailabilityService()
