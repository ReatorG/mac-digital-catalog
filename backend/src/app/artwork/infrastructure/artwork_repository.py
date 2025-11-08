import psycopg2
import psycopg2.extras
from typing import Optional, List, Dict, Any
from datetime import datetime


class ArtworkRepository:
    def __init__(self, db_conn):
        self.db = db_conn

    def create_artwork(self, artist_id: int, title: str, location: str,
                       series: Optional[str] = None,
                       year: Optional[int] = None,
                       specialty: Optional[str] = None,
                       technique: Optional[str] = None,
                       materials: Optional[str] = None,
                       image_url: Optional[str] = None,
                       assembly_criteria: Optional[str] = None,
                       description: Optional[str] = None,
                       bibliography: Optional[str] = None) -> Dict[str, Any]:
        cursor = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("""
            INSERT INTO artworks 
            (artist_id, title, series, year, specialty, technique, materials, location, image_url,
             assembly_criteria, description, bibliography, is_active, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE, %s)
            RETURNING id
        """, (artist_id, title, series, year, specialty, technique, materials, location,
              image_url, assembly_criteria, description, bibliography, datetime.now()))
        self.db.commit()

        artwork_id = cursor.fetchone()[0]
        return self.get_artwork_by_id(artwork_id)

    def get_artwork_by_id(self, artwork_id: int) -> Optional[Dict[str, Any]]:
        cursor = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("""
            SELECT a.*, ar.name AS artist_name, ar.surname AS artist_surname
            FROM artworks a
            LEFT JOIN artists ar ON a.artist_id = ar.id
            WHERE a.id = %s
        """, (artwork_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_all_artworks(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        cursor = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("""
            SELECT a.*, ar.name AS artist_name, ar.surname AS artist_surname
            FROM artworks a
            LEFT JOIN artists ar ON a.artist_id = ar.id
            ORDER BY a.id LIMIT %s OFFSET %s
        """, (limit, skip))
        return [dict(row) for row in cursor.fetchall()]

    def get_artworks_by_artist(self, artist_id: int) -> List[Dict[str, Any]]:
        cursor = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("""
            SELECT * FROM artworks WHERE artist_id = %s ORDER BY id
        """, (artist_id,))
        return [dict(row) for row in cursor.fetchall()]

    def update_artwork(self, artwork_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        cursor = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        set_clause = []
        params = []

        for key, value in kwargs.items():
            if value is not None and key in [
                'title', 'series', 'year', 'specialty', 'technique', 'materials',
                'location', 'image_url', 'assembly_criteria', 'description', 'bibliography'
            ]:
                set_clause.append(f"{key} = %s")
                params.append(value)

        if set_clause:
            set_clause.append("created_at = %s")
            params.append(datetime.now())
            params.append(artwork_id)

            query = f"UPDATE artworks SET {', '.join(set_clause)} WHERE id = %s"
            cursor.execute(query, params)
            self.db.commit()

        return self.get_artwork_by_id(artwork_id)

    def delete_artwork(self, artwork_id: int):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM artworks WHERE id = %s", (artwork_id,))
        self.db.commit()
        return {"deleted_id": artwork_id}
