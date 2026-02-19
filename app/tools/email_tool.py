from typing import Dict, Any
from app.services import email_service


def send_email_tool(state: Dict[str, Any]) -> str:
    to = state.get("to")
    subject = state.get("subject")
    body = state.get("body")
    if not all([to, subject, body]):
        return "Missing email parameters."
    success = email_service.send_email(to, subject, body)
    return "Email sent." if success else "Failed to send email."
