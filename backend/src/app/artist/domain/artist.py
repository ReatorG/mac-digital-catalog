from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from src.app.artwork.domain.artwork import Artwork

# forward reference to avoid circular imports
# (artworks will import Artist, and Artist references Artwork)
# type hints as strings solve that

@dataclass
class Artist:
    id: Optional[int]
    name: str
    surname: str
    apsav: bool
    pseudonym: Optional[str] = None
    birth_date: Optional[datetime] = None
    decease_date: Optional[datetime] = None
    image_url: Optional[str] = None
    gender: Optional[str] = None
    bibliography: Optional[str] = None
    biography: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None

    # relationship (optional list of artworks)
    artworks: Optional[List["Artwork"]] = None
