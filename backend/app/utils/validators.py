"""
Input validation functions
"""
import re
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Any, Dict, List, Optional

from app.core.config import settings


def is_non_empty_string(value: Any) -> bool:
    """Check whether a value is a non-empty string."""
    return isinstance(value, str) and bool(value.strip())


def is_valid_email(email: str) -> bool:
    """Validate email format."""
    if not is_non_empty_string(email):
        return False
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email.strip()) is not None


def is_valid_phone(phone: str) -> bool:
    """Validate phone number format."""
    if not is_non_empty_string(phone):
        return False
    # Simple validation: at least 10 digits
    digits = "".join(filter(str.isdigit, phone.strip()))
    return len(digits) >= 10


def parse_datetime_flexible(value: Any) -> Optional[datetime]:
    """Parse datetime using common clinic input formats.

    Supported string formats:
    - YYYY-MM-DD HH:MM
    - YYYY-MM-DD HH:MM:SS
    - YYYY-MM-DDTHH:MM
    - YYYY-MM-DDTHH:MM:SS
    """
    clinic_tz = ZoneInfo(settings.TIMEZONE or "Asia/Karachi")

    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=clinic_tz)

    if not is_non_empty_string(value):
        return None

    text = value.strip()
    allowed_formats = [
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%dT%H:%M:%S",
    ]

    for fmt in allowed_formats:
        try:
            parsed = datetime.strptime(text, fmt)
            return parsed.replace(tzinfo=clinic_tz)
        except ValueError:
            continue

    try:
        parsed_iso = datetime.fromisoformat(text)
        if parsed_iso.tzinfo is None:
            return parsed_iso.replace(tzinfo=clinic_tz)
        return parsed_iso.astimezone(clinic_tz)
    except ValueError:
        return None


def validate_appointment_date(value: Any) -> bool:
    """Validate appointment date is parseable and in the future."""
    parsed = parse_datetime_flexible(value)
    clinic_tz = ZoneInfo(settings.TIMEZONE or "Asia/Karachi")
    return bool(parsed and parsed > datetime.now(clinic_tz))


def _normalize_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "1"}
    return False


def _normalize_booking_extraction(data: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize booking extraction payload from LLM to expected keys."""
    normalized = {
        "patient_name": (data.get("patient_name") or "").strip() if isinstance(data.get("patient_name"), str) else "",
        "email": (data.get("email") or "").strip() if isinstance(data.get("email"), str) else "",
        "service": (data.get("service") or "").strip() if isinstance(data.get("service"), str) else "",
        "requested_date_text": (data.get("requested_date_text") or "").strip() if isinstance(data.get("requested_date_text"), str) else "",
        "requested_time_text": (data.get("requested_time_text") or "").strip() if isinstance(data.get("requested_time_text"), str) else "",
        "notes": (data.get("notes") or "").strip() if isinstance(data.get("notes"), str) else "",
        "followup_question": (data.get("followup_question") or "").strip() if isinstance(data.get("followup_question"), str) else "",
        "needs_followup": _normalize_bool(data.get("needs_followup")),
    }

    normalized_dt = data.get("normalized_datetime")
    parsed = parse_datetime_flexible(normalized_dt)
    normalized["normalized_datetime"] = parsed
    normalized["scheduled_time"] = parsed
    return normalized


def _is_valid_booking_time(value: datetime) -> bool:
    """Basic clinic-time guardrail for clearly invalid slots."""
    return 8 <= value.hour < 22


def validate_booking_details(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and normalize booking details for required fields and follow-up flow."""
    normalized = _normalize_booking_extraction(data)
    missing_fields: List[str] = []
    invalid_fields: List[str] = []

    patient_name = normalized.get("patient_name")
    if is_non_empty_string(patient_name):
        normalized["patient_name"] = patient_name.strip()
    else:
        normalized["patient_name"] = ""
        missing_fields.append("patient_name")

    email = normalized.get("email")
    if is_non_empty_string(email):
        normalized["email"] = email.strip()
        if not is_valid_email(normalized["email"]):
            invalid_fields.append("email")
    else:
        normalized["email"] = ""

    service = normalized.get("service")
    if is_non_empty_string(service):
        normalized["service"] = service.strip()
    else:
        normalized["service"] = ""
        missing_fields.append("service")

    raw_scheduled_time = normalized.get("scheduled_time")
    if not raw_scheduled_time:
        normalized["scheduled_time"] = None
        missing_fields.append("scheduled_time")
    else:
        parsed_scheduled_time = parse_datetime_flexible(raw_scheduled_time)
        clinic_tz = ZoneInfo(settings.TIMEZONE or "Asia/Karachi")
        if not parsed_scheduled_time:
            normalized["scheduled_time"] = None
            invalid_fields.append("scheduled_time")
        elif parsed_scheduled_time <= datetime.now(clinic_tz):
            normalized["scheduled_time"] = None
            invalid_fields.append("scheduled_time")
        elif not _is_valid_booking_time(parsed_scheduled_time):
            normalized["scheduled_time"] = None
            invalid_fields.append("scheduled_time")
        else:
            normalized["scheduled_time"] = parsed_scheduled_time
            normalized["normalized_datetime"] = parsed_scheduled_time

    # If LLM flagged ambiguity, enforce follow-up even if partial datetime exists.
    if normalized.get("needs_followup"):
        if not is_non_empty_string(normalized.get("followup_question", "")):
            normalized["followup_question"] = "Could you please confirm the exact date and time for your appointment?"

    if missing_fields or invalid_fields:
        normalized["needs_followup"] = True
        if not is_non_empty_string(normalized.get("followup_question", "")):
            normalized["followup_question"] = build_missing_booking_message(missing_fields, invalid_fields)

    is_valid = (
        len(missing_fields) == 0
        and len(invalid_fields) == 0
        and not normalized.get("needs_followup", False)
    )

    return {
        "is_valid": is_valid,
        "missing_fields": missing_fields,
        "invalid_fields": invalid_fields,
        "normalized_data": normalized,
    }


def build_missing_booking_message(missing_fields: List[str], invalid_fields: List[str]) -> str:
    """Build a friendly follow-up message for missing or invalid details."""
    if "scheduled_time" in invalid_fields:
        return "Please share a valid future appointment time within clinic hours (8 AM to 10 PM)."

    if "email" in invalid_fields:
        return "Please share a valid email address format, or continue without email."

    field_labels = {
        "patient_name": "your name",
        "service": "service",
        "scheduled_time": "date and time",
    }
    labels = [field_labels[field] for field in missing_fields if field in field_labels]

    if not labels:
        return "I can help with that booking. Please share your name, service, and date and time so I can schedule your appointment."

    if len(labels) == 1:
        details_text = labels[0]
    elif len(labels) == 2:
        details_text = f"{labels[0]} and {labels[1]}"
    else:
        details_text = ", ".join(labels[:-1]) + f", and {labels[-1]}"

    return f"I can help with that booking. Please share {details_text} so I can schedule your appointment."


def validate_booking_fields(data: Dict[str, Any]) -> tuple[bool, List[str], Dict[str, Any]]:
    """Backward-compatible wrapper around validate_booking_details."""
    result = validate_booking_details(data)
    combined_missing = list(result["missing_fields"])
    for field in result["invalid_fields"]:
        if field not in combined_missing:
            combined_missing.append(field)
    return result["is_valid"], combined_missing, result["normalized_data"]


__all__ = [
    "is_non_empty_string",
    "is_valid_email",
    "is_valid_phone",
    "parse_datetime_flexible",
    "validate_appointment_date",
    "validate_booking_details",
    "build_missing_booking_message",
    "validate_booking_fields",
]
