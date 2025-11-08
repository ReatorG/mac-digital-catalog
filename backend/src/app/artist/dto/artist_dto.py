from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime


# --- Request DTOs ---

class CreateArtistRequest(BaseModel):
    name: str
    surname: str
    apsav: bool = True
    pseudonym: Optional[str] = None
    birth_date: Optional[datetime] = None
    decease_date: Optional[datetime] = None
    image_url: Optional[HttpUrl] = None
    gender: Optional[str] = None
    bibliography: Optional[str] = None
    biography: Optional[str] = None


class UpdateArtistRequest(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    apsav: Optional[bool] = None
    pseudonym: Optional[str] = None
    birth_date: Optional[datetime] = None
    decease_date: Optional[datetime] = None
    image_url: Optional[HttpUrl] = None
    gender: Optional[str] = None
    bibliography: Optional[str] = None
    biography: Optional[str] = None


# --- Response DTOs ---

class ArtistResponse(BaseModel):
    id: int
    name: str
    surname: str
    apsav: bool
    pseudonym: Optional[str] = None
    birth_date: Optional[datetime] = None
    decease_date: Optional[datetime] = None
    image_url: Optional[HttpUrl] = None
    gender: Optional[str] = None
    bibliography: Optional[str] = None
    biography: Optional[str] = None
    is_active: bool
    created_at: datetime


class ArtistListResponse(BaseModel):
    artists: list[ArtistResponse]
    total: int
    page: int
    page_size: int
