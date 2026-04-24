from sqlalchemy import Column, String, Integer, DateTime
from app.db.base_class import Base
import uuid
from datetime import datetime

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, index=True)
    mentor_id = Column(String, index=True)
    student_id = Column(String, index=True)
    rating = Column(Integer) # 1-5
    review = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
