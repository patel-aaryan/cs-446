from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.dependencies.auth import get_current_user, security
from app.schemas.audio import AudioCreate, AudioUpdate, AudioResponse
from app.services import audio_service

router = APIRouter(prefix="/audio", tags=["Audio"])


@router.post("", response_model=AudioResponse, status_code=status.HTTP_201_CREATED, dependencies=[Security(security)])
async def create_audio(
    audio_data: AudioCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create audio for an image. Only the image creator can add audio."""
    return audio_service.create_audio(db, audio_data, current_user["id"])


@router.get("/{audio_id}", response_model=AudioResponse, dependencies=[Security(security)])
async def get_audio(
    audio_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get audio by ID. User must have access to the associated image's album."""
    return audio_service.get_audio(db, audio_id, current_user["id"])


@router.get("/image/{image_id}", response_model=AudioResponse, dependencies=[Security(security)])
async def get_audio_by_image(
    image_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get audio for a specific image. User must have access to the image's album."""
    return audio_service.get_audio_by_image(db, image_id, current_user["id"])


@router.put("/{audio_id}", response_model=AudioResponse, dependencies=[Security(security)])
async def update_audio(
    audio_id: int,
    audio_data: AudioUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update audio. Only the image creator can update."""
    return audio_service.update_audio(db, audio_id, audio_data, current_user["id"])


@router.delete("/{audio_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Security(security)])
async def delete_audio(
    audio_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete audio. Only the image creator can delete."""
    audio_service.delete_audio(db, audio_id, current_user["id"])
    return None

