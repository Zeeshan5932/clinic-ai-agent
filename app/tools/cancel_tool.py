from typing import Dict, Any
from app.db import models
from app.db.database import SessionLocal
from app.services import calendar_service, email_service


def cancel_appointment(state: Dict[str, Any]) -> str:
    """Tool to handle cancellation logic"""
    appt_id = state.get("appointment_id")

    db = SessionLocal()
    try:
        appt = db.query(models.Appointment).filter(models.Appointment.id == appt_id).first()
        if not appt:
            return "Appointment not found."
        appt.status = models.AppointmentStatus.cancelled
        db.commit()
        db.refresh(appt)
    finally:
        db.close()

    calendar_service.cancel_calendar_event(str(appt_id))
    email_service.send_email(
        to=f"{appt.patient_name}@example.com",
        subject="Appointment Cancelled",
        body=f"Your appointment on {appt.scheduled_time} has been cancelled.",
    )

    return f"Appointment {appt_id} has been cancelled."
