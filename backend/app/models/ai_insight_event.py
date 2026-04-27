from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base_class import Base

class AIInsightEvent(Base):
    __tablename__ = "ai_insight_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    insight_id = Column(String, index=True)
    action = Column(String) # 'view', 'apply', 'dismiss', 'click'
    confidence = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
