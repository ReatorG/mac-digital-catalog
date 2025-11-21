import psycopg
from typing import Optional, List, Dict, Any
from datetime import datetime


class ArtworkRepository:
    def __init__(self, db_conn):
        self.db = db_conn

    def create_artwork(
        self, artist_id: int, title: str, location: str,
        series: Optional[str] = None,
        year: Optional[int] = None,
        technique: Optional[str] = None,
        materials: Optional[str] = None,
        image_url: Optional[str] = None,
        description: Optional[str] = None,
        on_display: Optional[bool] = True
    ) -> Dict[str, Any]:

        cur = self.db.cursor()
        cur.execute("""
            INSERT INTO artworks 
            (artist_id, title, series, year, technique, materials, location,
             image_url, description, on_display, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            artist_id, title, series, year, technique, materials, location,
            image_url, description, on_display, datetime.now()
        ))
        self.db.commit()

        artwork_id = cur.fetchone()[0]
        cur.close()

        return self.get_artwork_by_id(artwork_id)

    def get_artwork_by_id(self, artwork_id: int) -> Optional[Dict[str, Any]]:
        cur = self.db.cursor()
        cur.execute("""
            SELECT a.*, ar.name AS artist_name, ar.surname AS artist_surname
            FROM artworks a
            LEFT JOIN artists ar ON a.artist_id = ar.id
            WHERE a.id = %s
        """, (artwork_id,))
        row = cur.fetchone()
        cur.close()
        return dict(row) if row else None

    def get_all_artworks(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        cur = self.db.cursor()
        cur.execute("""
            SELECT a.*, ar.name AS artist_name, ar.surname AS artist_surname
            FROM artworks a
            LEFT JOIN artists ar ON a.artist_id = ar.id
            ORDER BY a.id LIMIT %s OFFSET %s
        """, (limit, skip))
        rows = cur.fetchall()
        cur.close()
        return [dict(r) for r in rows]

    def get_artworks_by_artist(self, artist_id: int) -> List[Dict[str, Any]]:
        cur = self.db.cursor()
        cur.execute("SELECT * FROM artworks WHERE artist_id = %s ORDER BY id", (artist_id,))
        rows = cur.fetchall()
        cur.close()
        return [dict(r) for r in rows]

    def update_artwork(self, artwork_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        cur = self.db.cursor()

        allowed_fields = [
            'title', 'series', 'year',
            'technique', 'materials', 'location',
            'image_url', 'description', 'on_display'
        ]

        set_clause = []
        params = []

        for key, value in kwargs.items():
            if key in allowed_fields and value is not None:
                set_clause.append(f"{key} = %s")
                params.append(value)

        if set_clause:
            params.append(artwork_id)
            query = f"UPDATE artworks SET {', '.join(set_clause)} WHERE id = %s"
            cur.execute(query, params)
            self.db.commit()

        cur.close()
        return self.get_artwork_by_id(artwork_id)

    def delete_artwork(self, artwork_id: int):
        cur = self.db.cursor()
        cur.execute("DELETE FROM artworks WHERE id = %s", (artwork_id,))
        self.db.commit()
        cur.close()
        return {"deleted_id": artwork_id}

    def count_artworks(self):
        cur = self.db.cursor()
        cur.execute("SELECT COUNT(*) FROM artworks")
        total = cur.fetchone()['count']
        cur.close()
        return total
