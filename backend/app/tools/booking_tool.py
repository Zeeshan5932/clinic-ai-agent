"""
Booking tool - handles appointment booking logic
"""
from datetime import datetime
from typing import Dict, Any
from app.core.logging import logger
from app.db import models
from app.db.database import SessionLocal
from app.services import calendar_service, email_service


def book_appointment(state: Dict[str, Any]) -> str:
    """
    Book a new appointment.
    
    Expected state keys:
    - patient_name: str
    - service: str
    - scheduled_time: datetime
    """
    patient_name = state.get("patient_name")
    email = state.get("email")
    service_name = state.get("service")
    when = state.get("scheduled_time")
    notes = state.get("notes", "")

    # Validate inputs
    if not all([patient_name, email, service_name, when]):
        return "Error: Missing required booking information."

    db = SessionLocal()
    appt = None
    try:
        # Create appointment record
        appt = models.Appointment(
            patient_name=patient_name,
            email=email,
            service=service_name,
            scheduled_time=when,
            notes=notes,
        )
        db.add(appt)
        db.commit()
        db.refresh(appt)
        logger.info(f"Appointment {appt.id} booked for {patient_name}")

        # Try Google Calendar sync after the appointment is safely stored in DB.
        # Calendar failures are logged but do not fail the booking itself.
        try:
            event_id = calendar_service.create_calendar_event(
                patient_name=patient_name,
                service_name=service_name,
                start_datetime=when,
                description=(
                    f"Appointment ID: {appt.id}\n"
                    f"Patient Email: {email}\n"
                    f"Notes: {notes or 'N/A'}"
                ),
            )
            appt.google_event_id = event_id
            db.commit()
            db.refresh(appt)
            logger.info(f"Stored Google Calendar event ID for appointment {appt.id}: {event_id}")
        except Exception as calendar_error:
            db.rollback()
            logger.error(
                f"Appointment {appt.id} was saved, but Google Calendar sync failed: {calendar_error}"
            )
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to book appointment: {e}")
        return f"Error booking appointment: {str(e)}"
    finally:
        db.close()

    # Send confirmation email
    email_service.send_booking_confirmation_email(
        to_email=email,
        patient_name=patient_name,
        service_name=service_name,
        scheduled_time=when,
        appointment_id=appt.id,
    )

    return f"Appointment booked with ID {appt.id} for {patient_name} on {when}."


__all__ = ["book_appointment"]
