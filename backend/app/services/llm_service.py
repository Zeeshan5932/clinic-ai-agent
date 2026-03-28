"""
LLM Service - Handles all LLM provider interactions
Abstracted to support multiple providers (Groq, OpenAI, etc.)
"""
from langchain.llms import BaseLLM
from langchain_groq import ChatGroq
from app.core.config import settings
from app.core.logging import logger


def get_llm() -> BaseLLM:
    """
    Get configured LLM instance.
    Currently uses Groq, but can be extended to support other providers.
    """
    if not settings.GROQ_API_KEY:
        logger.warning("GROQ_API_KEY not set, LLM calls may fail")
    
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=settings.GROQ_MODEL,
        temperature=0.7,
    )


# Global LLM instance
llm = get_llm()
