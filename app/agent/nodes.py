from typing import Dict, Any
from langchain.llms import OpenAI
from app.config import settings
from app.agent import prompts
from app.agent.state import AgentState
from app.agent.router import intent_router
from app.tools import (
    booking_tool,
    reschedule_tool,
    cancel_tool,
    faq_tool,
)
# additional extraction prompts
DETAIL_PROMPT = {
    "booking": """
Extract the patient's name, service, and date/time from the message.
Respond in JSON with keys patient_name, service, scheduled_time (ISO format).
Message: {message}
""",
    "reschedule": """
Extract the appointment ID and new date/time from the message.
Respond in JSON with keys appointment_id (number), new_time (ISO format).
Message: {message}
""",
    "cancel": """
Extract the appointment ID from the message.
Respond in JSON with key appointment_id (number).
Message: {message}
""",
}
llm = OpenAI(model_name="gpt-4o", openai_api_key=settings.OPENAI_API_KEY)


def detect_intent(state: AgentState) -> AgentState:
    message = state.get("raw_message", "")
    prompt = prompts.INTENT_PROMPT.format(message=message)
    result = llm(prompt)
    # simple cleanup
    intent = result.strip().lower()
    if intent not in ["booking", "reschedule", "cancel", "faq"]:
        intent = "unknown"
    state["intent"] = intent
    return state


import json
from datetime import datetime


def _extract_details(state: AgentState, intent: str) -> AgentState:
    message = state.get("raw_message", "")
    prompt = DETAIL_PROMPT[intent].format(message=message)
    result = llm(prompt)
    try:
        data = json.loads(result)
    except Exception:
        # fallback empty
        data = {}
    # parse ISO datetimes if present
    if "scheduled_time" in data:
        try:
            data["scheduled_time"] = datetime.fromisoformat(data["scheduled_time"])
        except Exception:
            pass
    if "new_time" in data:
        try:
            data["new_time"] = datetime.fromisoformat(data["new_time"])
        except Exception:
            pass
    state.update(data)
    return state


def booking_node(state: AgentState) -> AgentState:
    state = _extract_details(state, "booking")
    state["response"] = booking_tool.book_appointment(state)
    return state


def reschedule_node(state: AgentState) -> AgentState:
    state = _extract_details(state, "reschedule")
    state["response"] = reschedule_tool.reschedule_appointment(state)
    return state


def cancel_node(state: AgentState) -> AgentState:
    state = _extract_details(state, "cancel")
    state["response"] = cancel_tool.cancel_appointment(state)
    return state


def faq_node(state: AgentState) -> AgentState:
    # state should contain question
    state["response"] = faq_tool.answer_faq(state)
    return state
