import logging

logger = logging.getLogger(__name__)

# trivial email sender

def send_email(to: str, subject: str, body: str) -> bool:
    logger.info(f"Sending email to {to}: {subject}\n{body}")
    # in production integrate with SMTP or transactional service
    return True
