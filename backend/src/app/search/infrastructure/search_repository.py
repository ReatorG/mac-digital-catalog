# backend/src/app/search/infrastructure/search_repository.py

from typing import List, Dict, Any

class SearchRepository:
    def __init__(self, db_conn):
        self.db = db_conn

    def search_artworks(self, query: str) -> List[Dict[str, Any]]:
        cur = self.db.cursor()
        like = f"%{query}%"

        cur.execute("""
            SELECT a.*, ar.name AS artist_name, ar.surname AS artist_surname
            FROM artworks a
            LEFT JOIN artists ar ON a.artist_id = ar.id
            WHERE LOWER(a.title) LIKE LOWER(%s)
               OR LOWER(ar.name) LIKE LOWER(%s)
               OR LOWER(ar.surname) LIKE LOWER(%s)
            ORDER BY a.id
        """, (like, like, like))

        rows = cur.fetchall()
        cur.close()
        return [dict(r) for r in rows]

    def search_artists(self, query: str) -> List[Dict[str, Any]]:
        cur = self.db.cursor()
        like = f"%{query}%"

        cur.execute("""
            SELECT *
            FROM artists
            WHERE LOWER(name) LIKE LOWER(%s)
               OR LOWER(surname) LIKE LOWER(%s)
            ORDER BY id
        """, (like, like))

        rows = cur.fetchall()
        cur.close()
        return [dict(r) for r in rows]
