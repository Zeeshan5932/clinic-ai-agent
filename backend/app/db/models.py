from sqlalchemy import Column, Integer, String, DateTime, Enum
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
    email = Column(String, nullable=True, index=True)
    service = Column(String, nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    notes = Column(String, nullable=True)
    google_event_id = Column(String, nullable=True, index=True)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.scheduled)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
