from fastapi import HTTPException, status
from typing import List, Dict, Any
from src.app.artist.infrastructure.artist_repository import ArtistRepository


class ArtistService:
    def __init__(self, repository: ArtistRepository):
        self.repository = repository

    def create_artist(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not data.get("name") or not data.get("surname"):
            raise HTTPException(400, "Artist name and surname are required")

        return self.repository.create_artist(
            name=data["name"],
            surname=data["surname"],
            birth_date=data.get("birth_date"),
            image_url=data.get("image_url"),
            gender=data.get("gender"),
            biography=data.get("biography"),
            active_artworks=data.get("active_artworks", True)
        )

    def get_artist_by_id(self, artist_id: int) -> Dict[str, Any]:
        artist = self.repository.get_artist_by_id(artist_id)
        if not artist:
            raise HTTPException(404, "Artist not found")
        return artist

    def get_all_artists(self, page: int = 1, page_size: int = 10):
        skip = (page - 1) * page_size
        artists = self.repository.get_all_artists(skip=skip, limit=page_size)
        return artists, len(artists)

    def update_artist(self, artist_id: int, data: Dict[str, Any]):
        self.get_artist_by_id(artist_id)
        return self.repository.update_artist(artist_id, **data)

    def delete_artist(self, artist_id: int):
        self.get_artist_by_id(artist_id)
        return self.repository.delete_artist(artist_id)
