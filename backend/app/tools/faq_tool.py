"""
FAQ tool - handles FAQ questions using LLM
"""
from typing import Dict, Any
from app.core.logging import logger
from app.services.llm_service import llm
from app.agent.prompts import FAQ_PROMPT


def answer_faq(state: Dict[str, Any]) -> str:
    """
    Answer a FAQ question using the LLM.
    
    Expected state keys:
    - question: str (or raw_message if question not provided)
    """
    question = state.get("question")
    
    # Fallback to raw_message if question not set
    if not question:
        question = state.get("raw_message", "")
    
    if not question:
        return "I didn't receive a question to answer."
    
    try:
        prompt = FAQ_PROMPT.format(question=question)
        result = llm.invoke(prompt)
        
        # Extract text content from result
        if hasattr(result, 'content'):
            response = result.content
        else:
            response = str(result)
        
        logger.info(f"FAQ answered: {question[:50]}...")
        return response
    except Exception as e:
        logger.error(f"Error answering FAQ: {e}")
        return f"I apologize, I couldn't answer that question at the moment."


__all__ = ["answer_faq"]
