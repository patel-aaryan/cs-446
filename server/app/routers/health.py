from fastapi import APIRouter
from app.controllers.health_controller import HealthController

router = APIRouter(prefix="/health", tags=["health"])
controller = HealthController()


@router.get("")
async def health_check():
    return controller.get_health()
