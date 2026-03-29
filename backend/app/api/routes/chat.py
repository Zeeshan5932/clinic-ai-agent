# """
# Chat API routes
# """
# from fastapi import APIRouter, HTTPException, status
# from app.schemas.chat import ChatRequest, ChatResponse
# from app.agent.graph import agent_graph
# from app.core.logging import logger

# router = APIRouter(
#     prefix="/api/v1/chat",
#     tags=["chat"],
# )


# @router.post("", response_model=ChatResponse)
# async def chat(request: ChatRequest):
#     """
#     Process user message through the AI receptionist agent.
#     """
#     try:
#         if not request.message or not request.message.strip():
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Message cannot be empty",
#             )
        
#         # Run pre-compiled agent graph
#         state = {"raw_message": request.message.strip()}

#         # Invoke graph and read final response from terminal state
#         final_state = agent_graph.invoke(state)
        
#         response = final_state.get("response", "Sorry, I couldn't process your request.")
#         logger.info(f"Chat request processed: {request.message[:50]}...")
        
#         return ChatResponse(response=response)
    
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"Unexpected error in chat endpoint: {e}", exc_info=True)
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Internal server error",
#         )


# __all__ = ["router"]


"""
Chat API routes
"""
from fastapi import APIRouter, HTTPException, status
from app.schemas.chat import ChatRequest, ChatResponse
from app.agent.graph import agent_graph
from app.core.logging import logger

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["chat"],
)

BOOKING_STATE_KEYS = (
    "patient_name",
    "email",
    "service",
    "requested_date_text",
    "requested_time_text",
    "normalized_datetime",
    "notes",
    "needs_followup",
    "followup_question",
)

# Simple in-memory session store
# Note: good for testing/dev only, not for production
SESSION_STORE = {}


def get_default_booking_state():
    return {
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


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process user message through the AI receptionist agent.
    """
    try:
        if not request.message or not request.message.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message cannot be empty",
            )

        # Use provided session_id if available, otherwise fallback
        session_id = getattr(request, "session_id", None) or "default"

        # Load previous session state
        session_data = SESSION_STORE.get(session_id, {})
        booking_state = session_data.get("booking_state", get_default_booking_state())

        # Flatten previous booking state into graph state so booking prompts can use it.
        state = {
            "raw_message": request.message.strip(),
            **booking_state,
        }

        # Invoke graph
        final_state = agent_graph.invoke(state)

        # Save updated booking fields for next turn.
        updated_booking_state = {
            key: final_state.get(key, booking_state.get(key, get_default_booking_state().get(key)))
            for key in BOOKING_STATE_KEYS
        }

        # Clear session booking context after successful completion.
        booking_completed = (
            final_state.get("intent") == "booking"
            and not updated_booking_state.get("needs_followup", False)
            and str(final_state.get("response", "")).startswith("Appointment booked with ID")
        )
        if booking_completed:
            updated_booking_state = get_default_booking_state()

        SESSION_STORE[session_id] = {
            "booking_state": updated_booking_state
        }

        response = final_state.get("response", "Sorry, I couldn't process your request.")
        logger.info(f"Chat request processed: {request.message[:50]}... | session_id={session_id}")

        return ChatResponse(response=response)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


__all__ = ["router"]