import psycopg
from psycopg.rows import dict_row
from src.app.config.settings import settings


def _init_tables(conn):
    """Create the basic tables if they don’t exist."""
    cur = conn.cursor()

    # Create artists table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS artists (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            surname VARCHAR(255) NOT NULL,
            birth_date TIMESTAMP,
            image_url TEXT,
            gender VARCHAR(50),
            biography TEXT,
            active_artworks BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)

    # Create artworks table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS artworks (
            id SERIAL PRIMARY KEY,
            artist_id INT REFERENCES artists(id) ON DELETE CASCADE,
            title VARCHAR(255) NOT NULL,
            series VARCHAR(255),
            year INT,
            technique VARCHAR(255),
            materials VARCHAR(255),
            location VARCHAR(255) NOT NULL,
            image_url TEXT,
            description TEXT,
            on_display BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)

    # Create comments table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id SERIAL PRIMARY KEY,
            artwork_id INT REFERENCES artworks(id) ON DELETE CASCADE,
            text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)


    conn.commit()
    cur.close()


def get_db():

    conn = psycopg.connect(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        dbname=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        row_factory=dict_row,   # each fetch returns dict instead of tuple
    )

    conn.autocommit = False

    # Create tables on startup only once
    _init_tables(conn)

    try:
        yield conn
    finally:
        conn.close()
