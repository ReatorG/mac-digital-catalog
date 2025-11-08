from fastapi import HTTPException, status
from typing import List, Dict, Any, Optional
from datetime import datetime
from src.app.artist.infrastructure.artist_repository import ArtistRepository


class ArtistService:
    def __init__(self, repository: ArtistRepository):
        self.repository = repository

    def create_artist(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new artist.
        - Name and surname are required.
        """
        if not data.get("name") or not data.get("surname"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Artist name and surname are required"
            )

        artist = self.repository.create_artist(
            name=data["name"],
            surname=data["surname"],
            apsav=data.get("apsav", True),
            pseudonym=data.get("pseudonym"),
            birth_date=data.get("birth_date"),
            decease_date=data.get("decease_date"),
            image_url=data.get("image_url"),
            gender=data.get("gender"),
            bibliography=data.get("bibliography"),
            biography=data.get("biography")
        )
        return artist

    def get_artist_by_id(self, artist_id: int) -> Dict[str, Any]:
        artist = self.repository.get_artist_by_id(artist_id)
        if not artist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artist not found"
            )
        return artist

    def get_all_artists(self, page: int = 1, page_size: int = 10) -> tuple[List[Dict[str, Any]], int]:
        skip = (page - 1) * page_size
        artists = self.repository.get_all_artists(skip=skip, limit=page_size)
        total = len(artists)
        return artists, total

    def update_artist(self, artist_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        artist = self.get_artist_by_id(artist_id)
        updated = self.repository.update_artist(artist_id, **data)
        return updated

    def delete_artist(self, artist_id: int) -> Dict[str, Any]:
        artist = self.get_artist_by_id(artist_id)
        if not artist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artist not found"
            )
        deleted = self.repository.delete_artist(artist_id)
        return deleted
