from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/example", tags=["Example"])


@router.get("/public")
async def public_endpoint():
    """This endpoint is accessible without authentication."""
    return {"message": "This is a public endpoint, anyone can access it"}


@router.get("/protected")
async def protected_endpoint(current_user: dict = Depends(get_current_user)):
    """This endpoint requires authentication.
    
    The current_user parameter will contain:
    - id: int
    - email: str
    - name: str
    - created_at: str
    """
    return {
        "message": f"Hello {current_user['name']}!",
        "user_info": current_user
    }
