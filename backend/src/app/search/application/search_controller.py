# backend/src/app/search/application/search_controller.py

from fastapi import APIRouter, Depends, Query
from src.app.database import get_db
from src.app.search.infrastructure.search_repository import SearchRepository
from src.app.search.domain.search_service import SearchService

router = APIRouter(prefix="/search", tags=["Search"])


def get_search_service(db=Depends(get_db)):
    return SearchService(SearchRepository(db))


# === Búsqueda paginada de obras ===
@router.get("/artworks")
def search_artworks(
    query: str = Query("", description="Texto a buscar"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    service: SearchService = Depends(get_search_service)
):
    artworks, total = service.search_artworks(query=query, page=page, page_size=page_size)
    return {
        "artworks": artworks,
        "total": total,
        "page": page,
        "page_size": page_size
    }


# === Búsqueda paginada de artistas ===
@router.get("/artists")
def search_artists(
    query: str = Query("", description="Texto a buscar"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    service: SearchService = Depends(get_search_service)
):
    artists, total = service.search_artists(query=query, page=page, page_size=page_size)
    return {
        "artists": artists,
        "total": total,
        "page": page,
        "page_size": page_size
    }
