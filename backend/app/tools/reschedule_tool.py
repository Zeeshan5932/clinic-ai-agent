"""
Reschedule tool - handles appointment rescheduling logic
"""
from datetime import datetime
from typing import Dict, Any
from app.core.logging import logger
from app.db import models
from app.db.database import SessionLocal
from app.services import calendar_service, email_service


def reschedule_appointment(state: Dict[str, Any]) -> str:
    """
    Reschedule an existing appointment.
    
    Expected state keys:
    - appointment_id: int
    - new_time: datetime
    """
    appt_id = state.get("appointment_id")
    new_time = state.get("new_time")

    # Validate inputs
    if not appt_id or not new_time:
        return "Error: Missing appointment ID or new time."

    db = SessionLocal()
    try:
        appt = db.query(models.Appointment).filter(
            models.Appointment.id == appt_id
        ).first()
        if not appt:
            return "Appointment not found."
        
        appt.scheduled_time = new_time
        db.commit()
        db.refresh(appt)
        logger.info(f"Appointment {appt_id} rescheduled to {new_time}")
    except Exception as e:
        logger.error(f"Failed to reschedule appointment: {e}")
        return f"Error rescheduling appointment: {str(e)}"
    finally:
        db.close()

    # Update calendar
    calendar_service.update_calendar_event(str(appt_id), new_time)

    # Send notification
    email_service.send_email(
        to=f"{appt.patient_name}@example.com",
        subject="Appointment Rescheduled",
        body=f"Your appointment has been moved to {new_time}.",
    )

    return f"Appointment {appt_id} rescheduled to {new_time}."


__all__ = ["reschedule_appointment"]
