from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON
from app.db.base_class import Base
import uuid
from datetime import datetime

class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), index=True)
    title = Column(String, nullable=False) # e.g. "Zero to FAANG Engineer"
    current_status = Column(String, default="In Progress")
    
    # Roadmap Milestones
    # [
    #   {"id": "m1", "title": "Master Data Structures", "status": "completed", "completed_at": "..."},
    #   {"id": "m2", "title": "System Design Patterns", "status": "pending"}
    # ]
    milestones = Column(JSON, nullable=False, default=list)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
