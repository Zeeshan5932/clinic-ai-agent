import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


def send_email(to: str, subject: str, body: str) -> bool:
    """
    Send an email. In production, integrate with SMTP or SendGrid.
    """
    logger.info(f"Sending email to {to}: {subject}")
    # In production, this would use SMTP or a service like SendGrid
    logger.debug(f"Email body:\n{body}")
    return True
