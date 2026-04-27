from sqlalchemy import Column, String, Integer, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import uuid

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    file_path = Column(String)
    analysis_results = Column(JSON, nullable=True) # AI feedback
    score = Column(Integer, default=0) # AI calculated score
    
    user = relationship("User", backref="resumes")
