from datetime import datetime
from typing import Dict, Any
from app.db import models
from app.db.database import SessionLocal
from app.services import calendar_service, email_service


def reschedule_appointment(state: Dict[str, Any]) -> str:
    """Tool to handle rescheduling logic"""
    appt_id = state.get("appointment_id")
    new_time = state.get("new_time")

    db = SessionLocal()
    try:
        appt = db.query(models.Appointment).filter(models.Appointment.id == appt_id).first()
        if not appt:
            return "Appointment not found."
        appt.scheduled_time = new_time
        db.commit()
        db.refresh(appt)
    finally:
        db.close()

    # simulate calendar update
    calendar_service.update_calendar_event(str(appt_id), new_time)

    email_service.send_email(
        to=f"{appt.patient_name}@example.com",
        subject="Appointment Rescheduled",
        body=f"Your appointment has been moved to {new_time}.",
    )

    return f"Appointment {appt_id} rescheduled to {new_time}."
