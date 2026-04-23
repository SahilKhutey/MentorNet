from sqlalchemy import Column, String, Enum, DateTime, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.constants import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    profile = relationship("Profile", back_populates="user", uselist=False)
