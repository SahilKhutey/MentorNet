from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from datetime import datetime
from app.core.database import Base

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, index=True)
    mentor_id = Column(Integer, index=True)

    start_time = Column(DateTime, index=True)
    end_time = Column(DateTime, index=True)

    status = Column(String, default="pending")  # pending / confirmed / completed / cancelled
    outcome = Column(String, nullable=True)     # success / neutral / failed

    created_at = Column(DateTime, default=datetime.utcnow)
