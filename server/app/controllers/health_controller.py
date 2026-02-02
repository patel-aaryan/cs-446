from fastapi import HTTPException
from app.services.health_service import HealthService


class HealthController:
    def __init__(self):
        self.service = HealthService()

    def get_health(self) -> dict:
        """Handle health check request."""
        result = self.service.check_health()

        if result["status"] == "unhealthy":
            raise HTTPException(status_code=503, detail=result)

        return result
