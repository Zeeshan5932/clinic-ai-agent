"""
LLM Prompts for the agent workflow
"""

INTENT_PROMPT = """
You are an intent classification model for a clinic AI receptionist.
Determine the user's intent from the message.
Return ONLY one of: booking, reschedule, cancel, faq

Message: {message}

Intent:"""

BOOKING_DETAIL_PROMPT = """
Extract patient booking details from the message.
Respond in JSON format with: patient_name, service, scheduled_time (ISO format YYYY-MM-DD HH:MM)

Message: {message}

JSON:"""

RESCHEDULE_DETAIL_PROMPT = """
Extract rescheduling details from the message.
Respond in JSON format with: appointment_id (number), new_time (ISO format YYYY-MM-DD HH:MM)

Message: {message}

JSON:"""

CANCEL_DETAIL_PROMPT = """
Extract cancellation details from the message.
Respond in JSON format with: appointment_id (number)

Message: {message}

JSON:"""

FAQ_PROMPT = """
You are a helpful clinic receptionist. Answer the following question concisely:
{question}"""

__all__ = [
    "INTENT_PROMPT",
    "BOOKING_DETAIL_PROMPT",
    "RESCHEDULE_DETAIL_PROMPT",
    "CANCEL_DETAIL_PROMPT",
    "FAQ_PROMPT",
]
