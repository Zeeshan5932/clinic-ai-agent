from typing import TypedDict, Optional, Any
from datetime import datetime

class AgentState(TypedDict, total=False):
    intent: str
    patient_name: str
    service: str
    scheduled_time: datetime
    appointment_id: int
    new_time: datetime
    question: str
    raw_message: str
    response: str
    # any additional fields as needed
