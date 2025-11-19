from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class Artist:
    id: Optional[int]
    name: str
    surname: str
    birth_date: Optional[datetime] = None
    image_url: Optional[str] = None
    gender: Optional[str] = None
    biography: Optional[str] = None
    active_artworks: bool = True
    created_at: Optional[datetime] = None

    artworks: Optional[List["Artwork"]] = None
