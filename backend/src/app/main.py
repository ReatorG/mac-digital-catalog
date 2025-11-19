from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.artist.application.artist_controller import router as artist_router
from src.app.artwork.application.artwork_controller import router as artwork_router
from src.app.config.settings import settings
from src.app.database import _init_tables
import psycopg

def create_app() -> FastAPI:
    app = FastAPI(
        title="Art Catalog API",
        version="1.0.0",
        description="Catálogo digital para el MAC.",
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
    # Startup event — create tables once
    # ==============================
    @app.on_event("startup")
    def startup_event():
        try:
            conn = psycopg.connect(
                host=settings.POSTGRES_HOST,
                port=settings.POSTGRES_PORT,
                dbname=settings.POSTGRES_DB,
                user=settings.POSTGRES_USER,
                password=settings.POSTGRES_PASSWORD,
            )
            _init_tables(conn)
            conn.close()
            print("Tables verified/created successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")

    # ==============================
    # Health Check Endpoint
    # ==============================
    @app.get("/health", tags=["Health"])
    async def health_check():
        try:
            conn = psycopg.connect(
                host=settings.POSTGRES_HOST,
                port=settings.POSTGRES_PORT,
                dbname=settings.POSTGRES_DB,
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
    app.include_router(artist_router, tags=["Artists"])
    app.include_router(artwork_router, tags=["Artworks"])

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
