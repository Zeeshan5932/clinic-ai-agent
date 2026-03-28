"""
Agent node implementations for the workflow
"""
import json
from datetime import datetime
from typing import Dict, Any

from app.agent import prompts
from app.agent.state import AgentState
from app.services.llm_service import llm
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
    
    # Parse JSON
    try:
        data = json.loads(result_text)
    except json.JSONDecodeError:
        data = {}
    
    # Parse datetime fields
    if "scheduled_time" in data and data["scheduled_time"]:
        try:
            data["scheduled_time"] = datetime.fromisoformat(data["scheduled_time"])
        except (ValueError, TypeError):
            pass
    
    if "new_time" in data and data["new_time"]:
        try:
            data["new_time"] = datetime.fromisoformat(data["new_time"])
        except (ValueError, TypeError):
            pass
    
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
