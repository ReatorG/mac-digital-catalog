from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

# --- Request DTOs ---

class CreateArtistRequest(BaseModel):
    name: str
    surname: str
    birth_date: Optional[datetime] = None
    image_url: Optional[HttpUrl] = None
    gender: Optional[str] = None
    biography: Optional[str] = None
    active_artworks: bool = True


class UpdateArtistRequest(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    birth_date: Optional[datetime] = None
    image_url: Optional[HttpUrl] = None
    gender: Optional[str] = None
    biography: Optional[str] = None
    active_artworks: Optional[bool] = None


# --- Response DTOs ---

class ArtistResponse(BaseModel):
    id: int
    name: str
    surname: str
    birth_date: Optional[datetime] = None
    image_url: Optional[HttpUrl] = None
    gender: Optional[str] = None
    biography: Optional[str] = None
    active_artworks: bool
    created_at: datetime


class ArtistListResponse(BaseModel):
    artists: list[ArtistResponse]
    total: int
    page: int
    page_size: int
