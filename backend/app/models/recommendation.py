from sqlalchemy import Column, Integer, Float, ForeignKey
from app.db.base_class import Base

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True) # The student/researcher receiving the rec
    mentor_id = Column(Integer, index=True) # The profile being recommended
    score = Column(Float)
