"""
Health Check Router

Provides a simple endpoint to verify that the API is running.
Useful for manual checks, uptime monitoring, and confirming the
server started correctly during local development.
"""

from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
def get_health() -> dict:
    """Return service health status and current UTC timestamp.

    Args:
        None.

    Returns:
        dict: Health payload containing:
            - status: "ok"
            - timestamp: UTC ISO 8601 timestamp

    Raises:
        None.

    Examples:
        GET /health
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }