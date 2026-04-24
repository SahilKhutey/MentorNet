from sqlalchemy import Column, String, DateTime
from app.db.base_class import Base
import uuid

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    mentor_id = Column(String, index=True)
    student_id = Column(String, index=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(String, default="scheduled")  # scheduled | completed | cancelled
