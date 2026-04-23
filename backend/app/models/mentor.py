from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Mentor(Base):
    __tablename__ = "mentors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    designation = Column(String) # Professor, PhD, etc.
    organization = Column(String) # University / Company
    experience_years = Column(Integer)
    h_index = Column(Integer, nullable=True)
    mentorship_types = Column(JSON) # ["Career Guidance", "Research Mentorship"]
    open_to_collaboration = Column(Boolean, default=True)
    availability_slots = Column(JSON) # Specific time slots
    
    user = relationship("User", backref="mentor_profile")
