"""WhatsApp session orchestration using the same website booking pipeline.

This service intentionally reuses the exact chat/agent extraction and booking flow,
so WhatsApp and website booking behavior remain consistent.
"""

from typing import Any

from app.agent.graph import agent_graph
from app.api.routes.chat import BOOKING_STATE_KEYS, get_default_booking_state
from app.core.logging import logger
from app.utils.validators import validate_booking_details

# In-memory session store keyed by sender phone number.
# Can be swapped with Redis/DB in future without changing webhook API.
SESSION_STORE: dict[str, dict[str, Any]] = {}


def get_or_create_session(phone: str) -> dict[str, Any]:
    """Return existing session or initialize a new one."""
    session = SESSION_STORE.get(phone)
    if not session:
        session = {"booking_state": get_default_booking_state()}
        SESSION_STORE[phone] = session
    return session


def reset_session(phone: str) -> None:
    """Reset booking context for a phone number."""
    SESSION_STORE[phone] = {"booking_state": get_default_booking_state()}


def _extract_booking_state_from_graph(final_state: dict[str, Any], fallback: dict[str, Any]) -> dict[str, Any]:
    return {
        key: final_state.get(key, fallback.get(key, get_default_booking_state().get(key)))
        for key in BOOKING_STATE_KEYS
    }


def process_user_message(phone: str, user_text: str) -> str:
    """Process WhatsApp text via the same graph used by website chat endpoint."""
    text = (user_text or "").strip()
    if not text:
        return "Please type your message so I can help with your booking."

    if text.upper() in {"CANCEL", "STOP"}:
        reset_session(phone)
        logger.info("WhatsApp session cancelled | phone=%s", phone)
        return "Your booking flow has been cancelled. Send a new message anytime to start again."

    session = get_or_create_session(phone)
    previous_booking_state = session.get("booking_state", get_default_booking_state())

    graph_state = {
        "raw_message": text,
        **previous_booking_state,
    }

    final_state = agent_graph.invoke(graph_state)
    response_text = final_state.get("response", "Sorry, I could not process your request.")

    updated_booking_state = _extract_booking_state_from_graph(final_state, previous_booking_state)
    session["booking_state"] = updated_booking_state
    SESSION_STORE[phone] = session

    parsed_data = {
        "patient_name": updated_booking_state.get("patient_name", ""),
        "email": updated_booking_state.get("email", ""),
        "service": updated_booking_state.get("service", ""),
        "requested_date_text": updated_booking_state.get("requested_date_text", ""),
        "requested_time_text": updated_booking_state.get("requested_time_text", ""),
        "normalized_datetime": updated_booking_state.get("normalized_datetime", ""),
        "notes": updated_booking_state.get("notes", ""),
        "needs_followup": updated_booking_state.get("needs_followup", False),
        "followup_question": updated_booking_state.get("followup_question", ""),
    }

    validation = validate_booking_details(parsed_data)
    missing_fields = validation.get("missing_fields", [])
    invalid_fields = validation.get("invalid_fields", [])

    logger.info("WhatsApp parsed data | phone=%s data=%s", phone, parsed_data)
    logger.info(
        "WhatsApp missing fields | phone=%s missing=%s invalid=%s",
        phone,
        missing_fields,
        invalid_fields,
    )

    booking_completed = (
        final_state.get("intent") == "booking"
        and not updated_booking_state.get("needs_followup", False)
        and str(response_text).startswith("Appointment booked with ID")
    )

    if validation.get("is_valid"):
        normalized_data = validation.get("normalized_data", {})
        final_booking_payload = {
            "patient_name": normalized_data.get("patient_name"),
            "email": normalized_data.get("email"),
            "service": normalized_data.get("service"),
            "scheduled_time": str(normalized_data.get("scheduled_time")),
            "notes": normalized_data.get("notes"),
        }
        logger.info("WhatsApp final booking payload | phone=%s payload=%s", phone, final_booking_payload)

    if booking_completed:
        logger.info("WhatsApp booking success | phone=%s response=%s", phone, response_text)
        reset_session(phone)
    elif final_state.get("intent") == "booking" and not updated_booking_state.get("needs_followup", False):
        logger.error("WhatsApp booking failure | phone=%s response=%s", phone, response_text)

    return response_text
