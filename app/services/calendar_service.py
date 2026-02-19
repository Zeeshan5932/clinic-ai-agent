import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# simulate booking calendar entries

def create_calendar_event(patient_name: str, service: str, when: datetime) -> str:
    # In a real system this would integrate with Google/Outlook/etc.
    logger.info(f"Creating calendar event for {patient_name} - {service} at {when}")
    return f"Calendar event created for {patient_name} on {when.isoformat()}"


def update_calendar_event(event_id: str, new_time: datetime) -> str:
    logger.info(f"Updating calendar event {event_id} to {new_time}")
    return f"Calendar event {event_id} updated to {new_time.isoformat()}"


def cancel_calendar_event(event_id: str) -> str:
    logger.info(f"Cancelling calendar event {event_id}")
    return f"Calendar event {event_id} cancelled"
