from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime


class CreateArtworkRequest(BaseModel):
    artist_id: int
    title: str
    location: str
    series: Optional[str] = None
    year: Optional[int] = None
    technique: Optional[str] = None
    materials: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    description: Optional[str] = None
    on_display: Optional[bool] = True


class UpdateArtworkRequest(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None
    series: Optional[str] = None
    year: Optional[int] = None
    technique: Optional[str] = None
    materials: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    description: Optional[str] = None
    on_display: Optional[bool] = None


class ArtworkResponse(BaseModel):
    id: int
    artist_id: int
    title: str
    location: str
    series: Optional[str]
    year: Optional[int]
    technique: Optional[str]
    materials: Optional[str]
    image_url: Optional[HttpUrl]
    description: Optional[str]
    on_display: bool
    created_at: datetime

    artist_name: Optional[str] = None
    artist_surname: Optional[str] = None


class ArtworkListResponse(BaseModel):
    artworks: list[ArtworkResponse]
    total: int
    page: int
    page_size: int
