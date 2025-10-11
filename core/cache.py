# core/cache.py
import sqlite3
from datetime import datetime, timedelta

class Cache:
    def __init__(self, db_path="cache.db", ttl_hours=24):
        self.db_path = db_path
        self.ttl = timedelta(hours=ttl_hours)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            query TEXT,
            url TEXT UNIQUE,
            title TEXT,
            snippet TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
        conn.close()

    def save(self, source, query, items):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        for item in items:
            url = item.get("url") or item.get("link")
            title = item.get("title") or "No title"
            snippet = item.get("snippet") or ""
            if not url:
                continue
            try:
                cursor.execute("""
                    INSERT INTO cache (source, query, url, title, snippet)
                    VALUES (?, ?, ?, ?, ?)
                """, (source, query, url, title, snippet))
            except sqlite3.IntegrityError:
                continue  # URL déjà présente
        conn.commit()
        conn.close()

    def load(self, query, source=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        expiration_time = datetime.now() - self.ttl
        if source:
            cursor.execute("""
                SELECT title, url, snippet FROM cache
                WHERE query=? AND source=? AND timestamp > ?
            """, (query, source, expiration_time))
        else:
            cursor.execute("""
                SELECT title, url, snippet FROM cache
                WHERE query=? AND timestamp > ?
            """, (query, expiration_time))
        rows = cursor.fetchall()
        conn.close()
        return [{"title": r[0], "url": r[1], "snippet": r[2]} for r in rows]
