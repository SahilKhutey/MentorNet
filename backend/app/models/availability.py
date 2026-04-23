from sqlalchemy import Column, Integer, DateTime, ForeignKey
from app.core.database import Base

class Availability(Base):
    __tablename__ = "availability"

    id = Column(Integer, primary_key=True, index=True)
    mentor_id = Column(Integer, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
