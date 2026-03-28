from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ChatRequest(BaseModel):
    message: str = Field(..., description="User message to the AI receptionist")


class ChatResponse(BaseModel):
    response: str = Field(..., description="AI receptionist response")


# Chat schema
__all__ = ["ChatRequest", "ChatResponse"]
