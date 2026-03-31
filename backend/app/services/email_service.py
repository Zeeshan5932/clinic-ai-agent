import smtplib
from datetime import datetime
from email.message import EmailMessage

from app.core.config import settings
from app.core.logging import logger


def _smtp_is_configured() -> bool:
    return all(
        [
            settings.SMTP_HOST,
            settings.SMTP_PORT,
            settings.SMTP_USER,
            settings.SMTP_PASSWORD,
            settings.EMAIL_FROM,
        ]
    )


def send_email(to: str, subject: str, body: str) -> bool:
    """Send email via SMTP. Returns False if SMTP is not configured or send fails."""
    if not to:
        logger.error("Cannot send email: recipient address is empty")
        return False

    if not _smtp_is_configured():
        logger.warning("SMTP is not fully configured. Skipping email delivery.")
        return False

    message = EmailMessage()
    from_name = settings.EMAIL_FROM_NAME or "Clinic Reception"
    message["From"] = f"{from_name} <{settings.EMAIL_FROM}>"
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            smtp.send_message(message)
        logger.info("Email sent successfully to %s", to)
        return True
    except Exception as exc:
        logger.error("Failed to send email to %s: %s", to, exc)
        return False


def send_booking_confirmation_email(
    to_email: str,
    patient_name: str,
    service_name: str,
    scheduled_time: datetime,
    appointment_id: int,
) -> bool:
    """Send a standardized booking confirmation message."""
    subject = f"Your Appointment is Confirmed | #{appointment_id}"
    body = (
        f"Dear {patient_name},\n\n"
        f"Great news. Your appointment has been successfully confirmed.\n\n"
        f"Appointment Details\n"
        f"- Appointment ID: {appointment_id}\n"
        f"- Service: {service_name}\n"
        f"- Date & Time: {scheduled_time}\n\n"
        f"If you need to reschedule or cancel, please reply to this email or contact us.\n\n"
        f"Warm regards,\n"
        f"{settings.EMAIL_FROM_NAME or 'Clinic Reception'}"
    )
    return send_email(to=to_email, subject=subject, body=body)


__all__ = ["send_email", "send_booking_confirmation_email"]
