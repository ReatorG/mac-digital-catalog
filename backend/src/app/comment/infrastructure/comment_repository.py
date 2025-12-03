# backend/src/app/comment/infrastructure/comment_repository.py

import psycopg
from typing import Dict, Any, List

class CommentRepository:
    def __init__(self, db_conn):
        self.db = db_conn

    def create_comment(self, artwork_id: int, text: str) -> Dict[str, Any]:
        cur = self.db.cursor()
        cur.execute("""
            INSERT INTO comments (artwork_id, text)
            VALUES (%s, %s)
            RETURNING id, artwork_id, text, created_at
        """, (artwork_id, text))

        row = cur.fetchone()
        self.db.commit()
        cur.close()
        return dict(row)

    def get_comments_by_artwork(self, artwork_id: int) -> List[Dict[str, Any]]:
        cur = self.db.cursor()
        cur.execute("""
            SELECT id, artwork_id, text, created_at
            FROM comments
            WHERE artwork_id = %s
            ORDER BY created_at DESC
        """, (artwork_id,))

        rows = cur.fetchall()
        cur.close()
        return [dict(r) for r in rows]
