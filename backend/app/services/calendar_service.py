import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def create_calendar_event(patient_name: str, service: str, when: datetime) -> str:
    """
    Create a calendar event. In production, integrate with Google Calendar/Outlook.
    """
    logger.info(f"Creating calendar event for {patient_name} - {service} at {when}")
    return f"Calendar event created for {patient_name} on {when.isoformat()}"


def update_calendar_event(event_id: str, new_time: datetime) -> str:
    """
    Update an existing calendar event.
    """
    logger.info(f"Updating calendar event {event_id} to {new_time}")
    return f"Calendar event {event_id} updated to {new_time.isoformat()}"


def cancel_calendar_event(event_id: str) -> str:
    """
    Cancel a calendar event.
    """
    logger.info(f"Cancelling calendar event {event_id}")
    return f"Calendar event {event_id} cancelled"
