"""
Agent node implementations for the workflow
"""
import json
from typing import Dict, Any

from app.agent import prompts
from app.agent.state import AgentState
from app.services.llm_service import llm
from app.utils.validators import (
    parse_datetime_flexible,
    validate_booking_details,
    build_missing_booking_message,
)
from app.tools import (
    booking_tool,
    reschedule_tool,
    cancel_tool,
    faq_tool,
)


def detect_intent(state: AgentState) -> AgentState:
    """
    Detect user intent using LLM.
    Returns one of: booking, reschedule, cancel, faq
    """
    message = state.get("raw_message", "")
    prompt = prompts.INTENT_PROMPT.format(message=message)
    result = llm.invoke(prompt)
    
    # Extract text content from result
    if hasattr(result, 'content'):
        intent = result.content.strip().lower()
    else:
        intent = str(result).strip().lower()
    
    # Validate intent
    if intent not in ["booking", "reschedule", "cancel", "faq"]:
        intent = "faq"
    
    state["intent"] = intent
    return state


def _strip_markdown_code_fences(text: str) -> str:
    """Strip markdown code fences if the model wraps JSON in them."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    return cleaned


def _safe_json_load(text: str, default_data: Dict[str, Any]) -> Dict[str, Any]:
    """Parse JSON safely and return default_data on failure."""
    try:
        parsed = json.loads(text)
        return parsed if isinstance(parsed, dict) else dict(default_data)
    except json.JSONDecodeError:
        return dict(default_data)


def _ensure_booking_keys(data: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure booking extraction always has exactly the required keys."""
    return {
        "patient_name": data.get("patient_name", "") or "",
        "email": data.get("email", "") or "",
        "service": data.get("service", "") or "",
        "requested_date_text": data.get("requested_date_text", "") or "",
        "requested_time_text": data.get("requested_time_text", "") or "",
        "normalized_datetime": data.get("normalized_datetime", "") or "",
        "notes": data.get("notes", "") or "",
        "needs_followup": data.get("needs_followup", False),
        "followup_question": data.get("followup_question", "") or "",
    }


def _extract_details(state: AgentState, intent: str) -> AgentState:
    """
    Extract structured details from user message using LLM.
    """
    message = state.get("raw_message", "")

    # Select appropriate prompt
    prompts_map = {
        "booking": prompts.BOOKING_DETAIL_PROMPT,
        "reschedule": prompts.RESCHEDULE_DETAIL_PROMPT,
        "cancel": prompts.CANCEL_DETAIL_PROMPT,
    }
    
    if intent not in prompts_map:
        return state
    
    prompt = prompts_map[intent].format(message=message)
    result = llm.invoke(prompt)
    
    # Extract text content
    if hasattr(result, 'content'):
        result_text = result.content
    else:
        result_text = str(result)

    cleaned_text = _strip_markdown_code_fences(result_text)

    # Parse JSON with safe defaults
    if intent == "booking":
        default_data: Dict[str, Any] = {
            "patient_name": "",
            "email": "",
            "service": "",
            "requested_date_text": "",
            "requested_time_text": "",
            "normalized_datetime": "",
            "notes": "",
            "needs_followup": False,
            "followup_question": "",
        }
    else:
        default_data = {}

    data = _safe_json_load(cleaned_text, default_data)

    if intent == "booking":
        data = _ensure_booking_keys(data)
    
    # Parse datetime fields
    if "normalized_datetime" in data and data["normalized_datetime"]:
        parsed_scheduled_time = parse_datetime_flexible(data["normalized_datetime"])
        if parsed_scheduled_time:
            data["normalized_datetime"] = parsed_scheduled_time
            data["scheduled_time"] = parsed_scheduled_time
    
    if "new_time" in data and data["new_time"]:
        parsed_new_time = parse_datetime_flexible(data["new_time"])
        if parsed_new_time:
            data["new_time"] = parsed_new_time
    
    # Convert appointment_id to int
    if "appointment_id" in data:
        try:
            data["appointment_id"] = int(data["appointment_id"])
        except (ValueError, TypeError):
            pass
    
    state.update(data)
    return state


def booking_node(state: AgentState) -> AgentState:
    """Handle appointment booking."""
    state = _extract_details(state, "booking")

    extracted = {
        "patient_name": state.get("patient_name", ""),
        "email": state.get("email", ""),
        "service": state.get("service", ""),
        "requested_date_text": state.get("requested_date_text", ""),
        "requested_time_text": state.get("requested_time_text", ""),
        "normalized_datetime": state.get("normalized_datetime", ""),
        "notes": state.get("notes", ""),
        "needs_followup": state.get("needs_followup", False),
        "followup_question": state.get("followup_question", ""),
    }
    validation = validate_booking_details(extracted)

    if not validation["is_valid"]:
        normalized_data = validation["normalized_data"]
        followup_question = normalized_data.get("followup_question")
        state["response"] = (
            followup_question
            if followup_question
            else build_missing_booking_message(
                validation["missing_fields"],
                validation["invalid_fields"],
            )
        )
        return state

    state.update(validation["normalized_data"])
    state["response"] = booking_tool.book_appointment(state)
    return state


def reschedule_node(state: AgentState) -> AgentState:
    """Handle appointment rescheduling."""
    state = _extract_details(state, "reschedule")
    state["response"] = reschedule_tool.reschedule_appointment(state)
    return state


def cancel_node(state: AgentState) -> AgentState:
    """Handle appointment cancellation."""
    state = _extract_details(state, "cancel")
    state["response"] = cancel_tool.cancel_appointment(state)
    return state


def faq_node(state: AgentState) -> AgentState:
    """Handle FAQ questions."""
    state["response"] = faq_tool.answer_faq(state)
    return state


__all__ = [
    "detect_intent",
    "booking_node",
    "reschedule_node",
    "cancel_node",
    "faq_node",
]
