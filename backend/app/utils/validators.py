"""
Input validation functions
"""
import re
from typing import Optional


def is_valid_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_valid_phone(phone: str) -> bool:
    """Validate phone number format."""
    # Simple validation: at least 10 digits
    digits = ''.join(filter(str.isdigit, phone))
    return len(digits) >= 10


def validate_appointment_date(date_str: str) -> bool:
    """Validate appointment date is in future."""
    from datetime import datetime
    try:
        date = datetime.fromisoformat(date_str)
        return date > datetime.now()
    except Exception:
        return False


__all__ = ["is_valid_email", "is_valid_phone", "validate_appointment_date"]
