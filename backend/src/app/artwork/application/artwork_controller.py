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


# ============================================================
# CREATE
# ============================================================

@router.post("/", response_model=ArtworkResponse, status_code=status.HTTP_201_CREATED)
def create_artwork(
    request: CreateArtworkRequest,
    service: ArtworkService = Depends(get_artwork_service)
):
    artwork = service.create_artwork(request.model_dump())
    return ArtworkResponse.model_validate(artwork)


# ============================================================
# LIST + FILTERS
# ============================================================

@router.get("/", response_model=ArtworkListResponse)
def list_artworks(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    query: str = Query("", description="Búsqueda por texto", alias="q"),
    order: str = Query("", description="Ordenamiento"),

    # RECIBEN string o lista DE FORMA SEGURA
    technique: Optional[list[str] | str] = Query(None, description="Filtrar por técnicas"),
    materials: Optional[list[str] | str] = Query(None, description="Filtrar por materiales"),
    location: Optional[list[str] | str] = Query(None, description="Filtrar por ubicaciones"),

    on_display: Optional[bool] = Query(None, description="Solo obras en exhibición"),
    service: ArtworkService = Depends(get_artwork_service)
):
    # --- NORMALIZACIÓN PARA QUE SIEMPRE SEAN LISTAS ---
    if isinstance(technique, str):
        technique = [technique]
    technique = technique or []

    if isinstance(materials, str):
        materials = [materials]
    materials = materials or []

    if isinstance(location, str):
        location = [location]
    location = location or []

    # --- LLAMADA AL SERVICIO ---
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



# ============================================================
# FILTER OPTIONS (MUST COME BEFORE /{artwork_id})
# ============================================================

@router.get("/filters")
def get_filters(service: ArtworkService = Depends(get_artwork_service)):
    """
    Devuelve las opciones disponibles para filtros:
    - locations
    - materials
    - techniques
    """
    return service.get_filter_options()


# ============================================================
# GET BY ARTIST
# ============================================================

@router.get("/artist/{artist_id}", response_model=list[ArtworkResponse])
def get_artworks_by_artist(
    artist_id: int,
    service: ArtworkService = Depends(get_artwork_service)
):
    artworks = service.get_artworks_by_artist(artist_id)
    return [ArtworkResponse.model_validate(a) for a in artworks]


# ============================================================
# GET BY ID (GENERIC ROUTE — MUST BE LAST)
# ============================================================

@router.get("/{artwork_id}", response_model=ArtworkResponse)
def get_artwork(
    artwork_id: int,
    service: ArtworkService = Depends(get_artwork_service)
):
    artwork = service.get_artwork_by_id(artwork_id)
    return ArtworkResponse.model_validate(artwork)


# ============================================================
# UPDATE
# ============================================================

@router.put("/{artwork_id}", response_model=ArtworkResponse)
def update_artwork(
    artwork_id: int,
    request: UpdateArtworkRequest,
    service: ArtworkService = Depends(get_artwork_service)
):
    updated = service.update_artwork(artwork_id, request.model_dump(exclude_unset=True))
    return ArtworkResponse.model_validate(updated)


# ============================================================
# DELETE
# ============================================================

@router.delete("/{artwork_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_artwork(
    artwork_id: int,
    service: ArtworkService = Depends(get_artwork_service)
):
    service.delete_artwork(artwork_id)
