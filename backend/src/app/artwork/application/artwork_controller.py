from fastapi import APIRouter, Depends, Query, status
from typing import Optional
from src.app.database import get_db
from src.app.artwork.infrastructure.artwork_repository import ArtworkRepository
from src.app.artist.infrastructure.artist_repository import ArtistRepository
from src.app.artwork.domain.artwork_service import ArtworkService
from src.app.artwork.dto.artwork_dto import (
    CreateArtworkRequest,
    UpdateArtworkRequest,
    ArtworkResponse,
    ArtworkListResponse
)

router = APIRouter(prefix="/artworks", tags=["Artworks"])


def get_artwork_service(db=Depends(get_db)) -> ArtworkService:
    artwork_repo = ArtworkRepository(db)
    artist_repo = ArtistRepository(db)
    return ArtworkService(artwork_repo, artist_repo)


@router.post("/", response_model=ArtworkResponse, status_code=status.HTTP_201_CREATED)
def create_artwork(
    request: CreateArtworkRequest,
    service: ArtworkService = Depends(get_artwork_service)
):
    artwork = service.create_artwork(request.model_dump())
    return ArtworkResponse.model_validate(artwork)


@router.get("/", response_model=ArtworkListResponse)
def list_artworks(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    query: str = Query("", description="Búsqueda por texto", alias="q"),
    order: str = Query("", description="Ordenamiento"),
    technique: list[str] = Query([], description="Filtrar por técnicas"),
    materials: list[str] = Query([], description="Filtrar por materiales"),
    location: list[str] = Query([], description="Filtrar por ubicaciones"),
    on_display: Optional[bool] = Query(None, description="Solo obras en exhibición"),
    service: ArtworkService = Depends(get_artwork_service)
):
    artworks, total = service.filter_artworks(
        page=page,
        page_size=page_size,
        query=query,
        order=order,
        technique=technique,
        materials=materials,
        location=location,
        on_display=on_display,
    )

    return ArtworkListResponse(
        artworks=[ArtworkResponse.model_validate(a) for a in artworks],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/artist/{artist_id}", response_model=list[ArtworkResponse])
def get_artworks_by_artist(
    artist_id: int,
    service: ArtworkService = Depends(get_artwork_service)
):
    artworks = service.get_artworks_by_artist(artist_id)
    return [ArtworkResponse.model_validate(a) for a in artworks]


@router.get("/{artwork_id}", response_model=ArtworkResponse)
def get_artwork(
    artwork_id: int,
    service: ArtworkService = Depends(get_artwork_service)
):
    artwork = service.get_artwork_by_id(artwork_id)
    return ArtworkResponse.model_validate(artwork)


@router.put("/{artwork_id}", response_model=ArtworkResponse)
def update_artwork(
    artwork_id: int,
    request: UpdateArtworkRequest,
    service: ArtworkService = Depends(get_artwork_service)
):
    updated = service.update_artwork(artwork_id, request.model_dump(exclude_unset=True))
    return ArtworkResponse.model_validate(updated)


@router.delete("/{artwork_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_artwork(
    artwork_id: int,
    service: ArtworkService = Depends(get_artwork_service)
):
    service.delete_artwork(artwork_id)

@router.get("/filters")
def get_filters(service: ArtworkService = Depends(get_artwork_service)):
    return service.get_all_filter_options()

@router.get("/filter-options")
def get_filter_options(db=Depends(get_db)):
    cur = db.cursor()

    def fetch_distinct(column):
        cur.execute(f"SELECT DISTINCT {column} FROM artworks WHERE {column} IS NOT NULL ORDER BY {column}")
        return [row[column] for row in cur.fetchall()]

    return {
        "locations": fetch_distinct("location"),
        "materials": fetch_distinct("materials"),
        "techniques": fetch_distinct("technique")
    }
