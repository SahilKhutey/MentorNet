from sqlalchemy import Column, String, Integer, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.models.tag import profile_tags

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    full_name = Column(String)
    bio = Column(String)
    location = Column(String)
    institution = Column(String)
    primary_field = Column(String)
    organization_id = Column(Integer, index=True, nullable=True)
    
    # AI Metadata
    embedding_id = Column(String, nullable=True)
    profile_score = Column(Integer, default=0)
    
    user = relationship("User", back_populates="profile")
    tags = relationship("Tag", secondary=profile_tags, back_populates="profiles")
    experience = relationship("Experience", back_populates="profile")
    publications = relationship("Publication", back_populates="profile")

class Experience(Base):
    __tablename__ = "experience"
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    title = Column(String)
    institution = Column(String)
    start_date = Column(String)
    end_date = Column(String, nullable=True)
    description = Column(Text)
    
    profile = relationship("Profile", back_populates="experience")

class Publication(Base):
    __tablename__ = "publications"
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    title = Column(String)
    journal = Column(String)
    year = Column(Integer)
    citation_count = Column(Integer, default=0)
    url = Column(String, nullable=True)
    
    profile = relationship("Profile", back_populates="publications")
