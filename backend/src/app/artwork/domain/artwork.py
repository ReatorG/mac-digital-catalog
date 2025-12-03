from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from src.app.artist.domain.artist import Artist

@dataclass
class Artwork:
    id: Optional[int]
    artist_id: int
    title: str
    location: str
    series: Optional[str] = None
    year: Optional[int] = None
    technique: Optional[str] = None
    materials: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    on_display: bool = True
    created_at: Optional[datetime] = None

    artist: Optional[Artist] = None
