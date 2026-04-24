from sqlalchemy import Column, String, DateTime
from app.core.database import Base
import uuid

class Availability(Base):
    __tablename__ = "availability"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    mentor_id = Column(String, index=True) # Linked to User.id (UUID)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
