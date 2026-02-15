from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import audio_repository, image_repository, album_repository, album_member_repository
from app.schemas.audio import AudioCreate, AudioUpdate, AudioResponse


def create_audio(db: Session, audio_data: AudioCreate, user_id: int) -> AudioResponse:
    """Create audio for an image. Only the image creator can add audio."""
    # Verify image exists and user is the creator
    image = image_repository.get_image_by_id(db, audio_data.image_id)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    # Check if user is the image creator
    if image["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the image creator can add audio"
        )
    
    # Check if audio already exists for this image
    existing_audio = audio_repository.get_audio_by_image_id(db, audio_data.image_id)
    if existing_audio:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Audio already exists for this image. Use update endpoint to modify it."
        )
    
    # Create the audio record
    audio = audio_repository.create_audio(
        db=db,
        image_id=audio_data.image_id,
        url=audio_data.url
    )
    
    if not audio:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create audio"
        )
    
    return AudioResponse(**audio)


def get_audio(db: Session, audio_id: int, user_id: int) -> AudioResponse:
    """Get audio by ID. User must have access to the associated image's album."""
    audio = audio_repository.get_audio_by_id(db, audio_id)
    if not audio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audio not found"
        )
    
    # Verify user has access to the image's album
    image = image_repository.get_image_by_id(db, audio["image_id"])
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associated image not found"
        )
    
    album = album_repository.get_album_by_id(db, image["album_id"])
    if not album:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album not found"
        )
    
    # Check if user is owner or member
    is_owner = album["owner_id"] == user_id
    is_member = album_member_repository.is_album_member(db, image["album_id"], user_id)
    
    if not (is_owner or is_member):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this audio"
        )
    
    return AudioResponse(**audio)


def get_audio_by_image(db: Session, image_id: int, user_id: int) -> AudioResponse:
    """Get audio for a specific image. User must have access to the image's album."""
    # Verify image exists and user has access
    image = image_repository.get_image_by_id(db, image_id)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    album = album_repository.get_album_by_id(db, image["album_id"])
    if not album:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album not found"
        )
    
    # Check if user is owner or member
    is_owner = album["owner_id"] == user_id
    is_member = album_member_repository.is_album_member(db, image["album_id"], user_id)
    
    if not (is_owner or is_member):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this image"
        )
    
    audio = audio_repository.get_audio_by_image_id(db, image_id)
    if not audio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No audio found for this image"
        )
    
    return AudioResponse(**audio)


def update_audio(db: Session, audio_id: int, audio_data: AudioUpdate, user_id: int) -> AudioResponse:
    """Update audio. Only the image creator can update."""
    audio = audio_repository.get_audio_by_id(db, audio_id)
    if not audio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audio not found"
        )
    
    # Verify user is the image creator
    image = image_repository.get_image_by_id(db, audio["image_id"])
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associated image not found"
        )
    
    if image["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the image creator can update the audio"
        )
    
    # Update the audio
    updated_audio = audio_repository.update_audio(
        db=db,
        audio_id=audio_id,
        url=audio_data.url
    )
    
    if not updated_audio:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update audio"
        )
    
    return AudioResponse(**updated_audio)


def delete_audio(db: Session, audio_id: int, user_id: int) -> None:
    """Delete audio. Only the image creator can delete."""
    audio = audio_repository.get_audio_by_id(db, audio_id)
    if not audio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audio not found"
        )
    
    # Verify user is the image creator
    image = image_repository.get_image_by_id(db, audio["image_id"])
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associated image not found"
        )
    
    if image["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the image creator can delete the audio"
        )
    
    success = audio_repository.delete_audio(db, audio_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete audio"
        )

