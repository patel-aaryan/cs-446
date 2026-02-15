"""
Cloudinary utility functions for generating upload signatures
Allows direct uploads from mobile clients without backend processing
"""
import cloudinary
import cloudinary.api
import cloudinary.utils
import time
from app.config.settings import get_settings

settings = get_settings()

# Configure Cloudinary
cloudinary.config(
    cloud_name=settings.cloudinary_cloud_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret
)


def generate_upload_signature(folder: str = "memento", resource_type: str = "auto") -> dict:
    """
    Generate upload signature for unsigned uploads from mobile clients.
    
    Args:
        folder: Folder path in Cloudinary (e.g., "memento/user_1")
        resource_type: "image", "video", "raw" (for audio), or "auto"
    
    Returns:
        dict with upload_url, timestamp, signature, and api_key
    """
    timestamp = int(time.time())
    
    # Parameters for upload
    params = {
        "timestamp": timestamp,
    }
    
    if folder:
        params["folder"] = folder
    
    # Use Cloudinary's utility to generate signature
    signature = cloudinary.utils.api_sign_request(params, settings.cloudinary_api_secret)
    
    return {
        "upload_url": f"https://api.cloudinary.com/v1_1/{settings.cloudinary_cloud_name}/{resource_type}/upload",
        "cloud_name": settings.cloudinary_cloud_name,
        "api_key": settings.cloudinary_api_key,
        "timestamp": timestamp,
        "signature": signature,
        "folder": folder
    }


def delete_asset(public_id: str, resource_type: str = "image") -> bool:
    """
    Delete an asset from Cloudinary (image, video, or audio).
    
    Args:
        public_id: The Cloudinary public_id of the asset
        resource_type: "image", "video", or "raw" (for audio)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        result = cloudinary.uploader.destroy(public_id, resource_type=resource_type)
        return result.get("result") == "ok"
    except Exception:
        return False

