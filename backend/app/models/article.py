from sqlalchemy import Column, String, Text, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime
import uuid

class Article(Base):
    __tablename__ = "articles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    author_id = Column(String, ForeignKey("users.id"))
    title = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    content = Column(Text)
    category = Column(String) # 'Research', 'PhD Advice', 'Technical', 'Career'
    views = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    author = relationship("User", backref="articles")
