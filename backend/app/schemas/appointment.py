from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class AppointmentStatus(str, Enum):
    scheduled = "scheduled"
    cancelled = "cancelled"
    completed = "completed"


class AppointmentBase(BaseModel):
    patient_name: str
    service: str
    scheduled_time: datetime


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    scheduled_time: Optional[datetime] = None
    status: Optional[AppointmentStatus] = None


class AppointmentResponse(AppointmentBase):
    id: int
    email: Optional[str] = None
    notes: Optional[str] = None
    google_event_id: Optional[str] = None
    status: AppointmentStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


__all__ = [
    "AppointmentBase",
    "AppointmentCreate",
    "AppointmentUpdate",
    "AppointmentResponse",
    "AppointmentStatus",
]
