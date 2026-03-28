from typing import TypedDict, Optional, Any
from datetime import datetime


class AgentState(TypedDict, total=False):
    """
    State schema for the AI agent workflow.
    Uses TypedDict for type safety across the LangGraph nodes.
    """
    intent: str
    patient_name: str
    service: str
    scheduled_time: datetime
    appointment_id: int
    new_time: datetime
    question: str
    raw_message: str
    response: str
