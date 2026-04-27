from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import uuid

# Association table for User Badges
user_badges = Table(
    "user_badges",
    Base.metadata,
    Column("user_id", String, ForeignKey("users.id"), primary_key=True),
    Column("badge_id", String, ForeignKey("badges.id"), primary_key=True)
)

class Badge(Base):
    __tablename__ = "badges"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True)
    icon = Column(String) # Icon name/URL
    description = Column(String)
    rarity = Column(String) # 'common', 'rare', 'elite'
    
    # Relationships
    users = relationship("User", secondary=user_badges, backref="badges")
