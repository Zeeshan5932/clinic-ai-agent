from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    message: str = Field(..., description="User message to the AI receptionist")
    session_id: Optional[str] = Field(
        default="default",
        description="Unique session ID for maintaining conversation state"
    )


class ChatResponse(BaseModel):
    response: str = Field(..., description="AI receptionist response")