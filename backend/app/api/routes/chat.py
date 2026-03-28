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
        
        # Run agent graph
        state = {"raw_message": request.message.strip()}
        
        # Compile and invoke graph
        compiled_graph = agent_graph.compile()
        final_state = compiled_graph.invoke(state)
        
        response = final_state.get("response", "Sorry, I couldn't process your request.")
        logger.info(f"Chat request processed: {request.message[:50]}...")
        
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
