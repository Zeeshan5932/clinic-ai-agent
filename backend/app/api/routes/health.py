"""
Health check API routes
"""
from fastapi import APIRouter
from app.schemas.common import HealthResponse
from app.core.config import settings

router = APIRouter(
    prefix="/api/v1/health",
    tags=["health"],
)


@router.get("", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        message=f"{settings.APP_NAME} is running",
    )


__all__ = ["router"]
