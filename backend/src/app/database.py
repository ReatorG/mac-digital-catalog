import psycopg2
from psycopg2.extras import RealDictCursor
from src.app.config.settings import settings


def _init_tables(conn):
    """Create the basic tables if they don’t exist."""
    cursor = conn.cursor()

    # Create artists table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artists (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            surname VARCHAR(255) NOT NULL,
            pseudonym VARCHAR(255),
            birth_date TIMESTAMP,
            decease_date TIMESTAMP,
            image_url TEXT,
            gender VARCHAR(50),
            apsav BOOLEAN NOT NULL,
            bibliography TEXT,
            biography TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)

    # Create artworks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artworks (
            id SERIAL PRIMARY KEY,
            artist_id INT REFERENCES artists(id) ON DELETE CASCADE,
            title VARCHAR(255) NOT NULL,
            series VARCHAR(255),
            year INT,
            specialty VARCHAR(255),
            technique VARCHAR(255),
            materials VARCHAR(255),
            location VARCHAR(255) NOT NULL,
            image_url TEXT,
            assembly_criteria TEXT,
            description TEXT,
            bibliography TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)

    conn.commit()
    cursor.close()


def get_db():
    """Provide a PostgreSQL connection."""
    conn = psycopg2.connect(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        database=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        cursor_factory=RealDictCursor,  # rows returned as dictionaries
    )
    conn.autocommit = False

    # Initialize tables once
    _init_tables(conn)

    try:
        yield conn
    finally:
        conn.close()
