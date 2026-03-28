"""
DateTime utilities
"""
from datetime import datetime, timedelta
from app.core.config import settings


def get_current_time() -> datetime:
    """Get current time in clinic timezone."""
    # In production, use pytz to handle timezones
    return datetime.now()


def add_days(date: datetime, days: int) -> datetime:
    """Add days to a datetime."""
    return date + timedelta(days=days)


def add_minutes(date: datetime, minutes: int) -> datetime:
    """Add minutes to a datetime."""
    return date + timedelta(minutes=minutes)


def is_within_hours(check_time: datetime, start_hour: int, end_hour: int) -> bool:
    """Check if time is within business hours."""
    return start_hour <= check_time.hour < end_hour


__all__ = [
    "get_current_time",
    "add_days",
    "add_minutes",
    "is_within_hours",
]
