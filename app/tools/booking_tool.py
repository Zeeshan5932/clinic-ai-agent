from datetime import datetime
from typing import Dict, Any
from app.db import models
from app.db.database import SessionLocal
from app.services import calendar_service, email_service


def book_appointment(state: Dict[str, Any]) -> str:
    """Tool to handle booking logic"""
    # expect state with patient_name, service, scheduled_time
    patient_name = state.get("patient_name")
    service_name = state.get("service")
    when = state.get("scheduled_time")

    db = SessionLocal()
    try:
        appt = models.Appointment(
            patient_name=patient_name,
            service=service_name,
            scheduled_time=when,
        )
        db.add(appt)
        db.commit()
        db.refresh(appt)
    finally:
        db.close()

    # simulate calendar
    calendar_service.create_calendar_event(patient_name, service_name, when)

    # send confirmation email (placeholder address)
    email_service.send_email(
        to=f"{patient_name}@example.com",
        subject="Appointment Confirmation",
        body=f"Your appointment for {service_name} on {when} has been confirmed.",
    )

    return f"Appointment booked with ID {appt.id} for {patient_name} on {when}."
