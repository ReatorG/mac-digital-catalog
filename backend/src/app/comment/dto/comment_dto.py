# backend/src/app/comment/dto/comment_dto.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CreateCommentRequest(BaseModel):
    artwork_id: int
    text: str

class CommentResponse(BaseModel):
    id: int
    artwork_id: int
    text: str
    created_at: datetime
