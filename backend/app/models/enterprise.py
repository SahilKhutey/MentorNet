from sqlalchemy import Column, Integer, String, DateTime, JSON
from app.core.database import Base
from datetime import datetime

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    domain = Column(String, unique=True) # e.g. "mit.edu"
    config = Column(JSON, nullable=True) # For custom theme/rules
    
    created_at = Column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    action = Column(String) # e.g. "LOGIN", "BOOKING_CONFIRMED"
    details = Column(JSON, nullable=True)
    ip_address = Column(String, nullable=True)
    
    timestamp = Column(DateTime, default=datetime.utcnow)
