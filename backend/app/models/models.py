from sqlalchemy import Column, Integer, String, DateTime, Text, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base

class InteractionType(str, enum.Enum):
    CALL = "call"
    MEETING = "meeting"
    EMAIL = "email"
    CONFERENCE = "conference"
    WEBINAR = "webinar"

class HCP(Base):
    __tablename__ = "hcps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    specialty = Column(String(255), nullable=True)
    organization = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=True)
    phone = Column(String(20), nullable=True)
    location = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    interactions = relationship("Interaction", back_populates="hcp", cascade="all, delete-orphan")

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_id = Column(Integer, ForeignKey("hcps.id"), nullable=False)
    interaction_type = Column(SQLEnum(InteractionType), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    hcp = relationship("HCP", back_populates="interactions")

class FollowUp(Base):
    __tablename__ = "follow_ups"

    id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(Integer, ForeignKey("interactions.id"), nullable=False)
    action_item = Column(String(500), nullable=False)
    due_date = Column(DateTime, nullable=True)
    completed = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
