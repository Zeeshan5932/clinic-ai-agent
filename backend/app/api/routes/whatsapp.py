"""Meta WhatsApp webhook routes."""

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse
from app.services.whatsapp_service import handle_incoming_whatsapp_message
from app.core.config import settings
from app.core.logging import logger

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])


@router.get("/webhook", response_class=PlainTextResponse)
async def verify_webhook(
    hub_mode: str | None = Query(default=None, alias="hub.mode"),
    hub_verify_token: str | None = Query(default=None, alias="hub.verify_token"),
    hub_challenge: str | None = Query(default=None, alias="hub.challenge"),
):
    """Meta verification endpoint for WhatsApp webhook setup."""
    if not settings.WHATSAPP_VERIFY_TOKEN:
        logger.error("WHATSAPP_VERIFY_TOKEN is not configured")
        raise HTTPException(status_code=500, detail="Webhook verify token is not configured")

    if hub_mode == "subscribe" and hub_verify_token == settings.WHATSAPP_VERIFY_TOKEN:
        return hub_challenge or ""

    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/webhook")
async def receive_whatsapp_webhook(request: Request):
    """Handle inbound WhatsApp message payloads and send text replies."""
    payload = await request.json()
    result = await handle_incoming_whatsapp_message(payload)

    return {
        "status": "ok",
        "processed": result.get("processed", 0),
        "replied": result.get("replied", 0),
    }
