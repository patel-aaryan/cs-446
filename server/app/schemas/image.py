from pydantic import BaseModel
from typing import Optional


class ImageCreate(BaseModel):
    album_id: int
    caption: Optional[str] = None
    image_url: str
    location: Optional[str] = None


class ImageUpdate(BaseModel):
    caption: Optional[str] = None
    image_url: Optional[str] = None
    location: Optional[str] = None


class ImageResponse(BaseModel):
    id: int
    album_id: int
    caption: Optional[str]
    image_url: str
    location: Optional[str]
    date_added: str
    user_id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

