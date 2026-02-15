from pydantic import BaseModel


class UploadSignatureResponse(BaseModel):
    """Response for generating upload signature for direct client uploads"""
    upload_url: str
    cloud_name: str
    api_key: str
    timestamp: int
    signature: str
    folder: str
