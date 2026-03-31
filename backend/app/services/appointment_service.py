"""Appointment service for WhatsApp-driven bookings.

This module is intentionally thin so it can be swapped with a DB-backed workflow
or a richer orchestration layer without changing webhook handlers.
"""

from datetime import datetime
from typing import Any

from app.tools.booking_tool import book_appointment


def _parse_datetime(date_text: str, time_text: str) -> datetime:
    """Parse date/time text from WhatsApp into a datetime object.

    Accepted examples:
    - date: 2026-04-10, 10/04/2026, 10-04-2026
    - time: 14:30, 2:30 PM, 2 PM
    """
    date_time_text = f"{date_text.strip()} {time_text.strip()}"
    formats = [
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %I:%M %p",
        "%Y-%m-%d %I %p",
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y %I:%M %p",
        "%d/%m/%Y %I %p",
        "%d-%m-%Y %H:%M",
        "%d-%m-%Y %I:%M %p",
        "%d-%m-%Y %I %p",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_time_text, fmt)
        except ValueError:
            continue

    raise ValueError(
        "Invalid date/time format. Use date like 2026-04-10 and time like 2:30 PM."
    )


def create_appointment_from_whatsapp(session: dict[str, Any]) -> dict[str, Any]:
    """Create an appointment from WhatsApp session data.

    Reuses existing booking logic so DB save, Google Calendar sync, and email
    notification behavior remain consistent with the rest of the application.
    """
    data = session.get("data", {})
    patient_name = (data.get("full_name") or "").strip()
    doctor = (data.get("doctor") or "").strip()
    date_text = (data.get("date") or "").strip()
    time_text = (data.get("time") or "").strip()
    reason = (data.get("reason") or "").strip()
    email = (data.get("email") or "").strip()

    if not all([patient_name, doctor, date_text, time_text, reason, email]):
        return {
            "success": False,
            "message": "Booking details are incomplete. Please restart and provide all fields.",
        }

    try:
        scheduled_time = _parse_datetime(date_text, time_text)
    except ValueError as exc:
        return {"success": False, "message": str(exc)}

    state = {
        "patient_name": patient_name,
        "service": doctor,
        "scheduled_time": scheduled_time,
        "notes": reason,
        "email": email,
    }

    booking_response = book_appointment(state)
    is_success = booking_response.lower().startswith("appointment booked")
    return {"success": is_success, "message": booking_response}
