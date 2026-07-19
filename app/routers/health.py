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
    """
    Provide a basic health check endpoint for the API.

    Returns:
        dict: A dictionary with:
            - "status": Always set to "ok" to indicate the API is running.
            - "timestamp": The current UTC time as an ISO 8601 string,
              providing the precise moment of the health check.

    Example response:
        {
            "status": "ok",
            "timestamp": "2024-06-03T12:34:56.789123+00:00"
        }
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }