

from sqlalchemy import Column, Integer, String, DateTime, Enum,Text
from sqlalchemy.sql import func
from app.db.database import Base
import enum


class AppointmentStatus(str, enum.Enum):
    scheduled = "scheduled"
    cancelled = "cancelled"
    completed = "completed"


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    service = Column(String, nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    notes = Column(Text, nullable=True)
    google_event_id = Column(String, nullable=True)
    status = Column(String, default="scheduled")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
