from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime
from src.app.artist.dto.artist_dto import ArtistResponse


# --- Request DTOs ---

class CreateArtworkRequest(BaseModel):
    artist_id: int
    title: str
    location: str
    series: Optional[str] = None
    year: Optional[int] = None
    specialty: Optional[str] = None
    technique: Optional[str] = None
    materials: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    assembly_criteria: Optional[str] = None
    description: Optional[str] = None
    bibliography: Optional[str] = None


class UpdateArtworkRequest(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None
    series: Optional[str] = None
    year: Optional[int] = None
    specialty: Optional[str] = None
    technique: Optional[str] = None
    materials: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    assembly_criteria: Optional[str] = None
    description: Optional[str] = None
    bibliography: Optional[str] = None


# --- Response DTOs ---

class ArtworkResponse(BaseModel):
    id: int
    artist_id: int
    title: str
    location: str
    series: Optional[str] = None
    year: Optional[int] = None
    specialty: Optional[str] = None
    technique: Optional[str] = None
    materials: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    assembly_criteria: Optional[str] = None
    description: Optional[str] = None
    bibliography: Optional[str] = None
    is_active: bool
    created_at: datetime

    # Optional nested artist info
    artist_name: Optional[str] = None
    artist_surname: Optional[str] = None

    def artist_summary(self) -> Optional[str]:
        if self.artist_name:
            return f"{self.artist_name} {self.artist_surname or ''}".strip()
        return None


class ArtworkListResponse(BaseModel):
    artworks: list[ArtworkResponse]
    total: int
    page: int
    page_size: int
