# backend/src/app/comment/domain/comment_service.py

from fastapi import HTTPException
from typing import Any, Dict, List
from src.app.comment.infrastructure.comment_repository import CommentRepository
from src.app.artwork.infrastructure.artwork_repository import ArtworkRepository


class CommentService:
    def __init__(self, comment_repo: CommentRepository, artwork_repo: ArtworkRepository):
        self.comment_repo = comment_repo
        self.artwork_repo = artwork_repo

    def create_comment(self, data: Dict[str, Any]):
        artwork_id = data.get("artwork_id")
        text = data.get("text")

        if not text:
            raise HTTPException(400, "Comment text is required")

        # validar que la obra existe
        artwork = self.artwork_repo.get_artwork_by_id(artwork_id)
        if not artwork:
            raise HTTPException(404, "Artwork not found")

        return self.comment_repo.create_comment(artwork_id, text)

    def get_comments_by_artwork(self, artwork_id: int):
        return self.comment_repo.get_comments_by_artwork(artwork_id)
