from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.artist.application.artist_controller import router as artist_router
from src.app.artwork.application.artwork_controller import router as artwork_router
from src.app.config.settings import settings
import psycopg2


def create_app() -> FastAPI:
    app = FastAPI(
        title="Art Catalog API",
        version="1.0.0",
        description="A simple digital catalog for artists and artworks.",
        swagger_ui_parameters={"persistAuthorization": True},
        openapi_tags=[
            {"name": "Health", "description": "Service health check"},
            {"name": "Artists", "description": "Artist management endpoints"},
            {"name": "Artworks", "description": "Artwork management endpoints"},
        ],
    )

    # ==============================
    # CORS Configuration
    # ==============================
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ==============================
    # Health Check Endpoint
    # ==============================
    @app.get("/health", tags=["Health"])
    async def health_check():
        """
        Health check endpoint to verify the database connection.
        """
        try:
            conn = psycopg2.connect(
                host=settings.POSTGRES_HOST,
                port=settings.POSTGRES_PORT,
                database=settings.POSTGRES_DB,
                user=settings.POSTGRES_USER,
                password=settings.POSTGRES_PASSWORD,
            )
            conn.close()
            return {
                "status": "healthy",
                "service": "art-catalog",
                "database": "connected",
                "version": "1.0.0",
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "service": "art-catalog",
                "database": "disconnected",
                "error": str(e),
                "version": "1.0.0",
            }

    # ==============================
    # Include Routers
    # ==============================
    app.include_router(artist_router, prefix="/api", tags=["Artists"])
    app.include_router(artwork_router, prefix="/api", tags=["Artworks"])

    # ==============================
    # Root Endpoint
    # ==============================
    @app.get("/", tags=["Health"])
    async def root():
        return {
            "message": "Welcome to the Art Catalog API 👋",
            "docs_url": "/docs",
            "endpoints": ["/api/artists", "/api/artworks"],
        }

    return app


app = create_app()
