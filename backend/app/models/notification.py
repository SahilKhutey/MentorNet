from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from app.db.base_class import Base
from datetime import datetime
import uuid

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    title = Column(String)
    message = Column(String)
    type = Column(String) # 'message', 'booking', 'ai_insight', 'system'
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
