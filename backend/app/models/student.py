from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    degree = Column(String) # BTech, MTech, etc.
    year_of_study = Column(Integer)
    learning_goals = Column(Text)
    career_goals = Column(Text)
    mentorship_type_needed = Column(String)
    
    user = relationship("User", backref="student_profile")
