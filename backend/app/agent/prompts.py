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
You are a booking information extractor for a clinic assistant.

Your job is to produce one merged booking JSON by combining PREVIOUS BOOKING STATE + CURRENT MESSAGE.

IMPORTANT:
- Return ONLY valid JSON.
- No markdown.
- No explanation.
- No extra keys.
- Always include every required key.
- If a value is unknown, use empty string "".
- needs_followup must be true or false (boolean, not string).

Use exactly these keys:
- patient_name
- email
- service
- requested_date_text
- requested_time_text
- normalized_datetime
- notes
- needs_followup
- followup_question

PREVIOUS BOOKING STATE:
{existing_state}

CURRENT MESSAGE:
{message}

Rules:
1. Read PREVIOUS BOOKING STATE first, then update it with any new details from CURRENT MESSAGE.
2. Keep prior non-empty values unless the user clearly changes/corrects them.
3. Never ask again for information that is already present and usable in merged state.
4. If CURRENT MESSAGE only adds date, keep prior time.
5. If CURRENT MESSAGE only adds time, keep prior date.
6. If CURRENT MESSAGE adds both date and time, update both.
7. requested_date_text and requested_time_text should keep latest user phrasing when provided.
8. Understand natural language date/time in Urdu, Roman Urdu, and English such as:
   - kal shaam 5 baje
   - next monday at 4 pm
   - Friday evening
   - aaj se 2 din baad morning
9. Default timezone is Asia/Karachi unless user explicitly gives another timezone.
10. normalized_datetime must be in ISO format: YYYY-MM-DDTHH:MM:SS+05:00 when confidently known.
11. If date is known but exact time is missing, set needs_followup=true and ask only for time.
12. If time is known but exact date is missing, set needs_followup=true and ask only for date.
13. If both date and time are known after merging previous + current context, then:
   - set needs_followup=false
   - set followup_question=""
14. Do not restart the booking flow.
15. Ask at most one follow-up item at a time, and only if still missing after merge.
16. If the user says something like "tomorrow evening", treat it as a date/time hint. If exact time is still needed, ask only for exact time.
17. If the user says something like "6:00 pm" after previously saying "tomorrow evening", preserve prior date and combine with new time.
18. If the user says something like "30-03-2026" after previously giving a time, preserve prior time and combine with new date.

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