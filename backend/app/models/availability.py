from sqlalchemy import Column, String, DateTime, Boolean
from app.db.base_class import Base
import uuid

class Availability(Base):
    __tablename__ = "availability"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    mentor_id = Column(String, index=True) # Linked to User.id (UUID)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_booked = Column(Boolean, default=False)
