import psycopg
from typing import Optional, List, Dict, Any
from datetime import datetime


class ArtistRepository:
    def __init__(self, db_conn):
        self.db = db_conn

    # ====================================
    # CREATE
    # ====================================
    def create_artist(
        self,
        name: str,
        surname: str,
        birth_date: Optional[datetime] = None,
        image_url: Optional[str] = None,
        gender: Optional[str] = None,
        biography: Optional[str] = None,
        active_artworks: bool = True
    ) -> Dict[str, Any]:

        cur = self.db.cursor()

        cur.execute(
            """
            INSERT INTO artists
            (name, surname, birth_date, image_url, gender, biography, active_artworks, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
            RETURNING id
            """,
            (
                name,
                surname,
                birth_date,
                image_url,
                gender,
                biography,
                active_artworks
            )
        )

        row = cur.fetchone()   # dict_row → {"id": X}
        self.db.commit()
        cur.close()

        artist_id = row["id"]
        return self.get_artist_by_id(artist_id)

    # ====================================
    # GET BY ID
    # ====================================
    def get_artist_by_id(self, artist_id: int) -> Optional[Dict[str, Any]]:
        cur = self.db.cursor()
        cur.execute("SELECT * FROM artists WHERE id = %s", (artist_id,))
        row = cur.fetchone()
        cur.close()
        return row if row else None   # row YA es dict

    # ====================================
    # GET ALL
    # ====================================
    def get_all_artists(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        cur = self.db.cursor()
        cur.execute(
            "SELECT * FROM artists ORDER BY id LIMIT %s OFFSET %s",
            (limit, skip)
        )
        rows = cur.fetchall()
        cur.close()
        return rows   # rows YA es List[Dict]

    # ====================================
    # UPDATE
    # ====================================
    def update_artist(self, artist_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        cur = self.db.cursor()

        allowed_fields = [
            "name", "surname", "birth_date", "image_url",
            "gender", "biography", "active_artworks"
        ]

        set_clause = []
        params = []

        for key, value in kwargs.items():
            if value is not None and key in allowed_fields:
                set_clause.append(f"{key} = %s")
                params.append(value)

        if set_clause:
            params.append(artist_id)
            query = f"UPDATE artists SET {', '.join(set_clause)} WHERE id = %s"
            cur.execute(query, params)
            self.db.commit()

        cur.close()
        return self.get_artist_by_id(artist_id)

    # ====================================
    # DELETE
    # ====================================
    def delete_artist(self, artist_id: int):
        cur = self.db.cursor()
        cur.execute("DELETE FROM artists WHERE id = %s", (artist_id,))
        self.db.commit()
        cur.close()
        return {"deleted_id": artist_id}
