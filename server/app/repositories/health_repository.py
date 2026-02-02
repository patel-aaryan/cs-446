from app.config.supabase import get_supabase


class HealthRepository:
    def __init__(self):
        self.supabase = get_supabase()

    def ping_database(self) -> str:
        """Execute a simple query to verify database connectivity."""
        response = self.supabase.rpc("heartbeat", {}).execute()
        return response
