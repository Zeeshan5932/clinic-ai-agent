"""
Cancel tool - handles appointment cancellation logic
"""
from typing import Dict, Any
from app.core.logging import logger
from app.db import models
from app.db.database import SessionLocal
from app.services import calendar_service, email_service


def cancel_appointment(state: Dict[str, Any]) -> str:
    """
    Cancel an existing appointment.
    
    Expected state keys:
    - appointment_id: int
    """
    appt_id = state.get("appointment_id")

    if not appt_id:
        return "Error: Appointment ID is required."

    db = SessionLocal()
    try:
        appt = db.query(models.Appointment).filter(
            models.Appointment.id == appt_id
        ).first()
        if not appt:
            return "Appointment not found."
        
        appt.status = models.AppointmentStatus.cancelled
        db.commit()
        db.refresh(appt)
        logger.info(f"Appointment {appt_id} cancelled")
    except Exception as e:
        logger.error(f"Failed to cancel appointment: {e}")
        return f"Error cancelling appointment: {str(e)}"
    finally:
        db.close()

    # Cancel calendar event
    calendar_service.cancel_calendar_event(str(appt_id))

    # Send notification
    email_service.send_email(
        to=f"{appt.patient_name}@example.com",
        subject="Appointment Cancelled",
        body=f"Your appointment on {appt.scheduled_time} has been cancelled.",
    )

    return f"Appointment {appt_id} has been cancelled."


__all__ = ["cancel_appointment"]
