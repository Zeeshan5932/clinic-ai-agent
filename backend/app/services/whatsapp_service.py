"""WhatsApp service for payload parsing and Cloud API replies."""

from typing import Any

import requests

from app.core.logging import logger
from app.core.config import settings
from app.services.whatsapp_session_service import process_user_message


def parse_incoming_messages(payload: dict[str, Any]) -> list[dict[str, str]]:
    """Extract sender/text messages from Meta webhook payload."""
    parsed: list[dict[str, str]] = []

    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            for message in value.get("messages", []):
                if message.get("type") != "text":
                    continue

                sender = message.get("from")
                text = (message.get("text") or {}).get("body", "").strip()
                if sender and text:
                    parsed.append({"sender": sender, "text": text})

    return parsed


def send_whatsapp_text(to: str, body: str) -> dict[str, Any]:
    """Send plain text reply to WhatsApp user via Cloud API."""
    if not settings.WHATSAPP_TOKEN or not settings.WHATSAPP_PHONE_NUMBER_ID:
        logger.error("WhatsApp Cloud credentials missing (WHATSAPP_TOKEN/WHATSAPP_PHONE_NUMBER_ID)")
        return {"ok": False, "error": "missing_whatsapp_credentials"}

    url = f"https://graph.facebook.com/v23.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": body},
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code >= 400:
            logger.error("WhatsApp send failed | to=%s status=%s body=%s", to, response.status_code, response.text)
            return {"ok": False, "status": response.status_code, "body": response.text}

        logger.info("WhatsApp send success | to=%s", to)
        return {"ok": True, "status": response.status_code}
    except Exception as exc:
        logger.error("WhatsApp send error | to=%s error=%s", to, exc)
        return {"ok": False, "error": str(exc)}


async def handle_incoming_whatsapp_message(payload: dict[str, Any]) -> dict[str, int]:
    """Handle inbound webhook payload and reply to each text message."""
    messages = parse_incoming_messages(payload)
    processed = 0
    replied = 0

    for item in messages:
        sender = item["sender"]
        user_text = item["text"]
        processed += 1

        logger.info("Incoming WhatsApp text | sender=%s text=%s", sender, user_text)

        try:
            reply_text = process_user_message(sender, user_text)
        except Exception as exc:
            logger.error("WhatsApp session processing error | sender=%s error=%s", sender, exc, exc_info=True)
            reply_text = "Sorry, we hit an internal error. Please try again."

        send_result = send_whatsapp_text(sender, reply_text)
        if send_result.get("ok"):
            replied += 1

    return {"processed": processed, "replied": replied}


# Backward-compatible alias used by earlier route versions.
handle_incoming_payload = handle_incoming_whatsapp_message
