from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from app.core.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, index=True)
    receiver_id = Column(Integer, index=True)
    content = Column(Text, nullable=False)
    
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Integer, default=0) # 0: unread, 1: read
