"""
Email tool - sends emails using the email service
"""
from typing import Dict, Any
from app.core.logging import logger
from app.services import email_service


def send_email_tool(state: Dict[str, Any]) -> str:
    """
    Send an email.
    
    Expected state keys:
    - to: str (email address)
    - subject: str
    - body: str
    """
    to = state.get("to")
    subject = state.get("subject")
    body = state.get("body")
    
    if not all([to, subject, body]):
        logger.warning("Missing email parameters")
        return "Missing email parameters."
    
    try:
        success = email_service.send_email(to, subject, body)
        if success:
            logger.info(f"Email sent to {to}")
            return "Email sent successfully."
        else:
            logger.error(f"Failed to send email to {to}")
            return "Failed to send email."
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return f"Error sending email: {str(e)}"


__all__ = ["send_email_tool"]
