# backend/src/app/comment/application/comment_controller.py

from fastapi import APIRouter, Depends, status
from src.app.database import get_db
from src.app.comment.infrastructure.comment_repository import CommentRepository
from src.app.artwork.infrastructure.artwork_repository import ArtworkRepository
from src.app.comment.domain.comment_service import CommentService
from src.app.comment.dto.comment_dto import CreateCommentRequest, CommentResponse

router = APIRouter(prefix="/comments", tags=["Comments"])


def get_comment_service(db=Depends(get_db)) -> CommentService:
    return CommentService(CommentRepository(db), ArtworkRepository(db))


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(request: CreateCommentRequest, service: CommentService = Depends(get_comment_service)):
    comment = service.create_comment(request.model_dump())
    return CommentResponse.model_validate(comment)


@router.get("/artwork/{artwork_id}", response_model=list[CommentResponse])
def list_comments(artwork_id: int, service: CommentService = Depends(get_comment_service)):
    return [
        CommentResponse.model_validate(c)
        for c in service.get_comments_by_artwork(artwork_id)
    ]
