from fastapi import HTTPException, status
from typing import List, Dict, Any
from src.app.artwork.infrastructure.artwork_repository import ArtworkRepository
from src.app.artist.infrastructure.artist_repository import ArtistRepository


class ArtworkService:
    def __init__(self, repository: ArtworkRepository, artist_repository: ArtistRepository):
        self.repository = repository
        self.artist_repository = artist_repository

    def create_artwork(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not data.get("title"):
            raise HTTPException(status_code=400, detail="Artwork title is required")

        if not data.get("location"):
            raise HTTPException(status_code=400, detail="Artwork location is required")

        artist_id = data.get("artist_id")
        artist = self.artist_repository.get_artist_by_id(artist_id)
        if not artist:
            raise HTTPException(status_code=400, detail=f"Artist {artist_id} does not exist")

        return self.repository.create_artwork(
            artist_id=artist_id,
            title=data["title"],
            location=data["location"],
            series=data.get("series"),
            year=data.get("year"),
            technique=data.get("technique"),
            materials=data.get("materials"),
            image_url=data.get("image_url"),
            description=data.get("description"),
            on_display=data.get("on_display", True),
        )

    def get_artwork_by_id(self, artwork_id: int) -> Dict[str, Any]:
        artwork = self.repository.get_artwork_by_id(artwork_id)
        if not artwork:
            raise HTTPException(status_code=404, detail="Artwork not found")
        return artwork

    def get_all_artworks(self, page: int = 1, page_size: int = 10):
        skip = (page - 1) * page_size
        artworks = self.repository.get_all_artworks(skip=skip, limit=page_size)
        return artworks, len(artworks)

    def get_artworks_by_artist(self, artist_id: int):
        artist = self.artist_repository.get_artist_by_id(artist_id)
        if not artist:
            raise HTTPException(status_code=404, detail="Artist not found")
        return self.repository.get_artworks_by_artist(artist_id)

    def update_artwork(self, artwork_id: int, data: Dict[str, Any]):
        self.get_artwork_by_id(artwork_id)
        return self.repository.update_artwork(artwork_id, **data)

    def delete_artwork(self, artwork_id: int):
        self.get_artwork_by_id(artwork_id)
        return self.repository.delete_artwork(artwork_id)

    def get_all_artworks(self, page: int = 1, page_size: int = 10):
        skip = (page - 1) * page_size
        artworks = self.repository.get_all_artworks(skip=skip, limit=page_size)

        total = self.repository.count_artworks()

        return artworks, total
