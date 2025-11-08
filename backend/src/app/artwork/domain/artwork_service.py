from fastapi import HTTPException, status
from typing import List, Dict, Any, Optional
from datetime import datetime
from src.app.artwork.infrastructure.artwork_repository import ArtworkRepository
from src.app.artist.infrastructure.artist_repository import ArtistRepository


class ArtworkService:
    def __init__(self, repository: ArtworkRepository, artist_repository: ArtistRepository):
        self.repository = repository
        self.artist_repository = artist_repository

    def create_artwork(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new artwork.
        - Must belong to an existing artist.
        - Requires a title and location.
        """
        if not data.get("title"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Artwork title is required"
            )

        if not data.get("location"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Artwork location is required"
            )

        artist_id = data.get("artist_id")
        artist = self.artist_repository.get_artist_by_id(artist_id)
        if not artist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Artist with id {artist_id} does not exist"
            )

        artwork = self.repository.create_artwork(
            artist_id=artist_id,
            title=data["title"],
            location=data["location"],
            series=data.get("series"),
            year=data.get("year"),
            specialty=data.get("specialty"),
            technique=data.get("technique"),
            materials=data.get("materials"),
            image_url=data.get("image_url"),
            assembly_criteria=data.get("assembly_criteria"),
            description=data.get("description"),
            bibliography=data.get("bibliography")
        )
        return artwork

    def get_artwork_by_id(self, artwork_id: int) -> Dict[str, Any]:
        artwork = self.repository.get_artwork_by_id(artwork_id)
        if not artwork:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artwork not found"
            )
        return artwork

    def get_all_artworks(self, page: int = 1, page_size: int = 10) -> tuple[List[Dict[str, Any]], int]:
        skip = (page - 1) * page_size
        artworks = self.repository.get_all_artworks(skip=skip, limit=page_size)
        total = len(artworks)
        return artworks, total

    def get_artworks_by_artist(self, artist_id: int) -> List[Dict[str, Any]]:
        artist = self.artist_repository.get_artist_by_id(artist_id)
        if not artist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artist not found"
            )
        artworks = self.repository.get_artworks_by_artist(artist_id)
        return artworks

    def update_artwork(self, artwork_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        artwork = self.get_artwork_by_id(artwork_id)
        updated = self.repository.update_artwork(artwork_id, **data)
        return updated

    def delete_artwork(self, artwork_id: int) -> Dict[str, Any]:
        artwork = self.get_artwork_by_id(artwork_id)
        deleted = self.repository.delete_artwork(artwork_id)
        return deleted
