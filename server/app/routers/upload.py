from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.dependencies.auth import get_current_user, security
from app.schemas.upload import UploadSignatureResponse
from app.utils.cloudinary_utils import generate_upload_signature

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.get("/signature/image", response_model=UploadSignatureResponse, dependencies=[Security(security)])
async def get_image_upload_signature(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get upload signature for direct image upload from mobile client.
    
    The client can use this signature to upload directly to Cloudinary,
    then send the resulting URL to the backend when creating an image record.
    """
    folder = f"memento/user_{current_user['id']}/images"
    signature_data = generate_upload_signature(folder=folder, resource_type="image")
    return UploadSignatureResponse(**signature_data)


@router.get("/signature/audio", response_model=UploadSignatureResponse, dependencies=[Security(security)])
async def get_audio_upload_signature(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get upload signature for direct audio upload from mobile client.
    
    Cloudinary supports audio files (MP3, WAV, FLAC, OGG, etc.).
    The client can use this signature to upload directly to Cloudinary,
    then send the resulting URL to the backend when creating an audio record.
    """
    folder = f"memento/user_{current_user['id']}/audio"
    signature_data = generate_upload_signature(folder=folder, resource_type="raw")
    return UploadSignatureResponse(**signature_data)

