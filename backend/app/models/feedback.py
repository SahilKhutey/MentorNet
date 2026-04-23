from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from datetime import datetime
from app.core.database import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, index=True)

    rating = Column(Float)  # 1–5
    review = Column(String)
    sentiment_score = Column(Float, nullable=True) # -1.0 to 1.0

    mentor_id = Column(Integer, index=True)
    student_id = Column(Integer, index=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
