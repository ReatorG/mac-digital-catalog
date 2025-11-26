import psycopg
from typing import Optional, List, Dict, Any
from datetime import datetime


class ArtworkRepository:
    def __init__(self, db_conn):
        self.db = db_conn

    # ============================================================
    # CREATE
    # ============================================================
    def create_artwork(
        self,
        artist_id: int, title: str, location: str,
        series: Optional[str] = None,
        year: Optional[int] = None,
        technique: Optional[str] = None,
        materials: Optional[str] = None,
        image_url: Optional[str] = None,
        description: Optional[str] = None,
        on_display: Optional[bool] = True
    ) -> Dict[str, Any]:

        cur = self.db.cursor()

        # Convertir HttpUrl a string si fuera necesario
        image_url = str(image_url) if image_url else None

        cur.execute("""
            INSERT INTO artworks 
            (artist_id, title, series, year, technique, materials, location,
             image_url, description, on_display, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            RETURNING id
        """, (
            artist_id, title, series, year, technique, materials, location,
            image_url, description, on_display
        ))

        row = cur.fetchone()     # dict_row
        self.db.commit()
        cur.close()

        artwork_id = row["id"]
        return self.get_artwork_by_id(artwork_id)

    # ============================================================
    # GET BY ID
    # ============================================================
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
        return row if row else None

    # ============================================================
    # GET ALL (pagination)
    # ============================================================
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
        return rows

    # ============================================================
    # GET BY ARTIST
    # ============================================================
    def get_artworks_by_artist(self, artist_id: int) -> List[Dict[str, Any]]:
        cur = self.db.cursor()
        cur.execute(
            """
            SELECT * FROM artworks 
            WHERE artist_id = %s 
            ORDER BY id
            """,
            (artist_id,)
        )
        rows = cur.fetchall()
        cur.close()
        return rows

    # ============================================================
    # UPDATE
    # ============================================================
    def update_artwork(self, artwork_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        cur = self.db.cursor()

        allowed_fields = [
            "title", "series", "year",
            "technique", "materials", "location",
            "image_url", "description", "on_display"
        ]

        set_clause = []
        params = []

        for key, value in kwargs.items():
            if value is not None and key in allowed_fields:

                # Convertir HttpUrl a str si viene del request
                if key == "image_url" and value:
                    value = str(value)

                set_clause.append(f"{key} = %s")
                params.append(value)

        if set_clause:
            params.append(artwork_id)
            query = f"""
                UPDATE artworks 
                SET {', '.join(set_clause)} 
                WHERE id = %s
            """
            cur.execute(query, params)
            self.db.commit()

        cur.close()
        return self.get_artwork_by_id(artwork_id)

    # ============================================================
    # DELETE
    # ============================================================
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

    def filter_artworks(self, query, order, technique, materials, location, on_display, skip, limit):
        cur = self.db.cursor()

        sql = """
            SELECT a.*, ar.name AS artist_name, ar.surname AS artist_surname
            FROM artworks a
            LEFT JOIN artists ar ON a.artist_id = ar.id
            WHERE 1=1
        """

        params = []

        if query:
            sql += " AND (LOWER(a.title) LIKE LOWER(%s) OR LOWER(ar.name) LIKE LOWER(%s) OR LOWER(ar.surname) LIKE LOWER(%s))"
            like = f"%{query}%"
            params += [like, like, like]

        if technique:
            sql += " AND LOWER(a.technique) = ANY(%s)"
            params.append([t.lower() for t in technique])

        if materials:
            sql += " AND LOWER(a.materials) = ANY(%s)"
            params.append([m.lower() for m in materials])

        if location:
            sql += " AND LOWER(a.location) = ANY(%s)"
            params.append([l.lower() for l in location])

        if on_display is not None:
            sql += " AND a.on_display = %s"
            params.append(on_display)

        # Ordenamiento
        order_map = {
            "title_asc": "a.title ASC",
            "title_desc": "a.title DESC",
            "year_asc": "a.year ASC NULLS LAST",
            "year_desc": "a.year DESC NULLS LAST",
        }
        if order in order_map:
            sql += " ORDER BY " + order_map[order]
        else:
            sql += " ORDER BY a.id"

        sql += " LIMIT %s OFFSET %s"
        params += [limit, skip]

        cur.execute(sql, params)
        rows = cur.fetchall()
        cur.close()
        return rows

    def count_filtered_artworks(self, query, technique, materials, location, on_display):
        cur = self.db.cursor()

        sql = "SELECT COUNT(*) FROM artworks a LEFT JOIN artists ar ON a.artist_id = ar.id WHERE 1=1"
        params = []

        if query:
            sql += " AND (LOWER(a.title) LIKE LOWER(%s) OR LOWER(ar.name) LIKE LOWER(%s) OR LOWER(ar.surname) LIKE LOWER(%s))"
            like = f"%{query}%"
            params += [like, like, like]

        if technique:
            sql += " AND LOWER(a.technique) LIKE LOWER(%s)"
            params.append(f"%{technique}%")

        if materials:
            sql += " AND LOWER(a.materials) LIKE LOWER(%s)"
            params.append(f"%{materials}%")

        if location:
            sql += " AND LOWER(a.location) LIKE LOWER(%s)"
            params.append(f"%{location}%")

        if on_display is not None:
            sql += " AND a.on_display = %s"
            params.append(on_display)

        cur.execute(sql, params)
        total = cur.fetchone()["count"]
        cur.close()
        return total

    def get_filter_options(self):
        cur = self.db.cursor()

        cur.execute("SELECT DISTINCT location FROM artworks WHERE location IS NOT NULL")
        locations = [r["location"] for r in cur.fetchall()]

        cur.execute("SELECT DISTINCT materials FROM artworks WHERE materials IS NOT NULL")
        materials = [r["materials"] for r in cur.fetchall()]

        cur.execute("SELECT DISTINCT technique FROM artworks WHERE technique IS NOT NULL")
        techniques = [r["technique"] for r in cur.fetchall()]

        cur.close()

        return {
            "locations": locations,
            "materials": materials,
            "techniques": techniques
        }
