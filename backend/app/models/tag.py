from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base_class import Base

# Association table for Many-to-Many relationship between Profile and Tags
profile_tags = Table(
    "profile_tags",
    Base.metadata,
    Column("profile_id", Integer, ForeignKey("profiles.id")),
    Column("tag_id", Integer, ForeignKey("tags.id"))
)

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True) # e.g. "Computer Vision", "Python"
    category = Column(String) # e.g. "Research Field", "Skill"
    
    profiles = relationship("Profile", secondary=profile_tags, back_populates="tags")
