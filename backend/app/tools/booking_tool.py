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
    service_name = state.get("service")
    when = state.get("scheduled_time")

    # Validate inputs
    if not all([patient_name, service_name, when]):
        return "Error: Missing required booking information."

    db = SessionLocal()
    try:
        # Create appointment record
        appt = models.Appointment(
            patient_name=patient_name,
            service=service_name,
            scheduled_time=when,
        )
        db.add(appt)
        db.commit()
        db.refresh(appt)
        logger.info(f"Appointment {appt.id} booked for {patient_name}")
    except Exception as e:
        logger.error(f"Failed to book appointment: {e}")
        return f"Error booking appointment: {str(e)}"
    finally:
        db.close()

    # Simulate calendar integration
    calendar_service.create_calendar_event(patient_name, service_name, when)

    # Send confirmation email
    email_service.send_email(
        to=f"{patient_name}@example.com",
        subject="Appointment Confirmation",
        body=f"Your appointment for {service_name} on {when} has been confirmed.",
    )

    return f"Appointment booked with ID {appt.id} for {patient_name} on {when}."


__all__ = ["book_appointment"]
