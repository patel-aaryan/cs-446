from pydantic import BaseModel
from typing import Optional


class AudioCreate(BaseModel):
    image_id: int
    url: str


class AudioUpdate(BaseModel):
    url: Optional[str] = None


class AudioResponse(BaseModel):
    id: int
    image_id: int
    url: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

