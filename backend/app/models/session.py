from sqlalchemy import Column, String, DateTime, JSON, Text
from app.db.base_class import Base
import uuid
from datetime import datetime

class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    booking_id = Column(String, index=True)
    mentor_id = Column(String, index=True)
    student_id = Column(String, index=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    meeting_link = Column(String, nullable=True)
    status = Column(String, default="upcoming")  # upcoming | live | completed | cancelled
    
    # AI Generated Content
    ai_summary = Column(Text, nullable=True)
    ai_insights = Column(JSON, nullable=True) # List of strings
    
    created_at = Column(DateTime, default=datetime.utcnow)
