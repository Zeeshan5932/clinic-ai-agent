from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from google.oauth2 import service_account
from googleapiclient.discovery import build

from app.core.logging import logger
from app.core.config import settings

GOOGLE_CALENDAR_SCOPES = ["https://www.googleapis.com/auth/calendar"]
_calendar_service = None


def _resolve_credentials_path(credentials_file: str) -> Path:
    """Resolve credentials path from absolute, CWD-relative, backend-relative, or project-root-relative inputs."""
    candidate = Path(credentials_file)
    if candidate.is_absolute():
        return candidate

    # 1) Try path as provided relative to current working directory.
    cwd_candidate = candidate.resolve()
    if cwd_candidate.exists():
        return cwd_candidate

    # 2) Try path relative to backend directory.
    backend_dir = Path(__file__).resolve().parents[2]
    backend_candidate = (backend_dir / candidate).resolve()
    if backend_candidate.exists():
        return backend_candidate

    # 3) Try path relative to project root.
    project_root = backend_dir.parent
    project_candidate = (project_root / candidate).resolve()
    if project_candidate.exists():
        return project_candidate

    # Fall back to backend-relative path for a clear error message in caller.
    return backend_candidate


def _ensure_timezone_aware(start_datetime: datetime) -> datetime:
    """Ensure datetime has timezone info using configured clinic timezone."""
    timezone = ZoneInfo(settings.TIMEZONE)
    if start_datetime.tzinfo is None:
        return start_datetime.replace(tzinfo=timezone)
    return start_datetime.astimezone(timezone)


def get_calendar_service():
    """Build and cache Google Calendar API service client."""
    global _calendar_service

    if _calendar_service is not None:
        return _calendar_service

    if not settings.GOOGLE_CALENDAR_CREDENTIALS_FILE:
        raise ValueError("GOOGLE_CALENDAR_CREDENTIALS_FILE is not configured")
    if not settings.GOOGLE_CALENDAR_ID:
        raise ValueError("GOOGLE_CALENDAR_ID is not configured")

    credentials_path = _resolve_credentials_path(settings.GOOGLE_CALENDAR_CREDENTIALS_FILE)
    if not credentials_path.exists():
        raise FileNotFoundError(f"Google credentials file not found: {credentials_path}")

    credentials = service_account.Credentials.from_service_account_file(
        str(credentials_path),
        scopes=GOOGLE_CALENDAR_SCOPES,
    )

    _calendar_service = build("calendar", "v3", credentials=credentials, cache_discovery=False)
    return _calendar_service


def create_calendar_event(
    patient_name: str,
    service_name: str,
    start_datetime: datetime,
    duration_minutes: int | None = None,
    description: str = "",
) -> str:
    """Create an event in Google Calendar and return the generated Google event ID."""
    calendar_service = get_calendar_service()

    start_at = _ensure_timezone_aware(start_datetime)
    event_duration = duration_minutes or settings.DEFAULT_APPOINTMENT_DURATION_MINUTES
    end_at = start_at + timedelta(minutes=event_duration)

    event_payload = {
        "summary": f"{service_name} - {patient_name}",
        "description": description or f"Appointment for {patient_name}",
        "start": {
            "dateTime": start_at.isoformat(),
            "timeZone": settings.TIMEZONE,
        },
        "end": {
            "dateTime": end_at.isoformat(),
            "timeZone": settings.TIMEZONE,
        },
    }

    event = (
        calendar_service.events()
        .insert(calendarId=settings.GOOGLE_CALENDAR_ID, body=event_payload)
        .execute()
    )

    event_id = event.get("id")
    if not event_id:
        raise RuntimeError("Google Calendar event was created without an event ID")

    logger.info(
        "Google Calendar event created successfully: patient=%s event_id=%s",
        patient_name,
        event_id,
    )
    return event_id


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
    if not event_id:
        raise ValueError("Google Calendar event_id is required")

    calendar_service = get_calendar_service()
    calendar_service.events().delete(
        calendarId=settings.GOOGLE_CALENDAR_ID,
        eventId=event_id,
    ).execute()
    logger.info("Google Calendar event cancelled successfully: event_id=%s", event_id)
    return f"Calendar event {event_id} cancelled"
