from fastapi import APIRouter, Depends, Query, status
from typing import Optional
from src.app.database import get_db
from src.app.artist.infrastructure.artist_repository import ArtistRepository
from src.app.artist.domain.artist_service import ArtistService
from src.app.artist.dto.artist_dto import (
    CreateArtistRequest,
    UpdateArtistRequest,
    ArtistResponse,
    ArtistListResponse
)

router = APIRouter(prefix="/artists", tags=["Artists"])


def get_artist_service(db=Depends(get_db)) -> ArtistService:
    repository = ArtistRepository(db)
    return ArtistService(repository)


@router.post("/", response_model=ArtistResponse, status_code=status.HTTP_201_CREATED)
def create_artist(
    request: CreateArtistRequest,
    service: ArtistService = Depends(get_artist_service)
):
    """
    Crear un nuevo artista.
    """
    artist = service.create_artist(request.model_dump())
    return ArtistResponse.model_validate(artist)


@router.get("/", response_model=ArtistListResponse)
def list_artists(
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, description="Registros por página"),
    service: ArtistService = Depends(get_artist_service)
):
    """
    Listar artistas con paginación.
    """
    artists, total = service.get_all_artists(page=page, page_size=page_size)
    return ArtistListResponse(
        artists=[ArtistResponse.model_validate(a) for a in artists],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{artist_id}", response_model=ArtistResponse)
def get_artist(
    artist_id: int,
    service: ArtistService = Depends(get_artist_service)
):
    """
    Obtener un artista por ID.
    """
    artist = service.get_artist_by_id(artist_id)
    return ArtistResponse.model_validate(artist)


@router.put("/{artist_id}", response_model=ArtistResponse)
def update_artist(
    artist_id: int,
    request: UpdateArtistRequest,
    service: ArtistService = Depends(get_artist_service)
):
    """
    Actualizar información de un artista.
    """
    updated = service.update_artist(artist_id, request.model_dump(exclude_unset=True))
    return ArtistResponse.model_validate(updated)


@router.delete("/{artist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_artist(
    artist_id: int,
    service: ArtistService = Depends(get_artist_service)
):
    """
    Eliminar un artista.
    """
    service.delete_artist(artist_id)
