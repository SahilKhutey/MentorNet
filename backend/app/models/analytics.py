from sqlalchemy import Column, Integer, Float
from app.core.database import Base

class MentorAnalytics(Base):
    __tablename__ = "mentor_analytics"

    mentor_id = Column(Integer, primary_key=True, index=True)

    avg_rating = Column(Float, default=0)
    sentiment_avg = Column(Float, default=0) # -1.0 to 1.0
    total_sessions = Column(Integer, default=0)
    success_rate = Column(Float, default=0)
    contribution_score = Column(Float, default=0) # Calculated rank
