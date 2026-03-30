"""
FAQ tool - handles FAQ questions using LLM
"""
from typing import Dict, Any
from app.core.logging import logger
from app.services.llm_service import llm
from app.agent.prompts import FAQ_PROMPT


def _answer_fee_question(question: str) -> str | None:
    text = (question or "").lower()
    pricing_markers = ("fee", "fees", "price", "prices", "cost", "charges", "charge", "package", "estimate")
    if not any(marker in text for marker in pricing_markers):
        return None

    consultation_line = "Dermatologist consultation fee: PKR 2,500. Follow-up within 14 days: PKR 1,500."
    treatment_lines = [
        "Hydra Facial: PKR 6,500",
        "Acne Treatment Session: PKR 4,000",
        "Chemical Peel: PKR 7,500",
        "Laser Hair Removal: from PKR 5,000",
        "Skin Brightening Therapy: PKR 8,500",
        "Microneedling: PKR 9,000",
    ]

    if "consult" in text or "doctor" in text:
        return (
            f"{consultation_line} "
            "If you want, I can also guide you for the right treatment plan and estimated total sessions."
        )

    if any(keyword in text for keyword in ["acne", "hydra", "peel", "laser", "brightening", "microneedling", "skin"]):
        return (
            "Here are current skin treatment fees: "
            + "; ".join(treatment_lines)
            + ". Final cost can vary after doctor assessment."
        )

    return (
        f"{consultation_line} "
        "Common treatment fees: "
        + "; ".join(treatment_lines)
        + ". Final charges depend on assessment and session plan."
    )


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

    fee_answer = _answer_fee_question(question)
    if fee_answer:
        logger.info("FAQ fee answer served without LLM")
        return fee_answer
    
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
