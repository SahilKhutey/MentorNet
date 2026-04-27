from sqlalchemy import Column, Integer, String, ForeignKey, Table, Float
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    category = Column(String, index=True) # e.g., 'technical', 'research', 'soft'

class UserSkill(Base):
    __tablename__ = "user_skills"

    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), primary_key=True)
    level = Column(Integer, default=1) # 1-5
    endorsements = Column(Integer, default=0)
