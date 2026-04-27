from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import uuid

# Association table for Lab Members
lab_members = Table(
    "lab_members",
    Base.metadata,
    Column("lab_id", String, ForeignKey("labs.id"), primary_key=True),
    Column("user_id", String, ForeignKey("users.id"), primary_key=True)
)

class Lab(Base):
    __tablename__ = "labs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, index=True)
    pi_id = Column(String, ForeignKey("users.id")) # Principal Investigator
    institution = Column(String)
    description = Column(String, nullable=True)
    
    # Relationships
    pi = relationship("User", foreign_keys=[pi_id])
    members = relationship("User", secondary=lab_members, backref="labs")
