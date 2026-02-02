from app.repositories.health_repository import HealthRepository


class HealthService:
    def __init__(self):
        self.repository = HealthRepository()

    def check_health(self) -> dict:
        """Check overall system health including database connectivity."""
        try:
            response = self.repository.ping_database()
            return {"status": response, "database": "connected"}
        except Exception as e:
            return {"status": "unhealthy", "database": str(e)}
