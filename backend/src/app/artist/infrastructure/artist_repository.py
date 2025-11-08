import psycopg2
import psycopg2.extras
from typing import Optional, List, Dict, Any
from datetime import datetime


class ArtistRepository:
    def __init__(self, db_conn):
        self.db = db_conn

    def create_artist(self, name: str, surname: str, apsav: bool,
                      pseudonym: Optional[str] = None,
                      birth_date: Optional[datetime] = None,
                      decease_date: Optional[datetime] = None,
                      image_url: Optional[str] = None,
                      gender: Optional[str] = None,
                      bibliography: Optional[str] = None,
                      biography: Optional[str] = None) -> Dict[str, Any]:
        cursor = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("""
            INSERT INTO artists 
            (name, surname, pseudonym, birth_date, decease_date, image_url, gender, apsav, bibliography, biography, is_active, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE, %s)
            RETURNING id
        """, (name, surname, pseudonym, birth_date, decease_date, image_url,
              gender, apsav, bibliography, biography, datetime.now()))
        self.db.commit()

        artist_id = cursor.fetchone()[0]
        return self.get_artist_by_id(artist_id)

    def get_artist_by_id(self, artist_id: int) -> Optional[Dict[str, Any]]:
        cursor = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM artists WHERE id = %s", (artist_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_all_artists(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        cursor = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM artists ORDER BY id LIMIT %s OFFSET %s", (limit, skip))
        return [dict(row) for row in cursor.fetchall()]

    def update_artist(self, artist_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        cursor = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        set_clause = []
        params = []

        for key, value in kwargs.items():
            if value is not None and key in [
                'name', 'surname', 'pseudonym', 'birth_date', 'decease_date',
                'image_url', 'gender', 'apsav', 'bibliography', 'biography'
            ]:
                set_clause.append(f"{key} = %s")
                params.append(value)

        if set_clause:
            set_clause.append("created_at = %s")
            params.append(datetime.now())
            params.append(artist_id)

            query = f"UPDATE artists SET {', '.join(set_clause)} WHERE id = %s"
            cursor.execute(query, params)
            self.db.commit()

        return self.get_artist_by_id(artist_id)

    def delete_artist(self, artist_id: int):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM artists WHERE id = %s", (artist_id,))
        self.db.commit()
        return {"deleted_id": artist_id}
