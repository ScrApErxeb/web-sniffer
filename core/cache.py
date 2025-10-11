# core/cache.py
import sqlite3
from datetime import datetime, timedelta

class Cache:
    """
    Gestion d'un cache SQLite avec TTL pour éviter de rescraper.
    Chaque entrée a : source, query, url, title, snippet et timestamp.
    """
    def __init__(self, db_path="cache.db", ttl_seconds=3600):
        self.db_path = db_path
        self.ttl = ttl_seconds
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

    def save(self, source: str, query: str, results: list):
        """
        Sauvegarde une liste de résultats dans le cache.
        results = [{"title": ..., "url": ..., "snippet": ...}, ...]
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        now = datetime.utcnow()
        for item in results:
            url = item.get("url")
            title = item.get("title", "No title")
            snippet = item.get("snippet", "")
            if not url:
                continue
            try:
                cursor.execute("""
                    INSERT OR REPLACE INTO cache (source, query, url, title, snippet, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (source, query, url, title, snippet, now))
            except sqlite3.IntegrityError:
                continue
        conn.commit()
        conn.close()

    def load(self, query: str, source: str = None):
        """
        Charge les résultats valides (non expirés) pour une query et optionnellement une source.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        expiry = datetime.utcnow() - timedelta(seconds=self.ttl)
        expiry_str = expiry.strftime("%Y-%m-%d %H:%M:%S")

        if source:
            cursor.execute("""
                SELECT title, url, snippet FROM cache
                WHERE query=? AND source=? AND timestamp > ?
            """, (query, source, expiry_str))
        else:
            cursor.execute("""
                SELECT title, url, snippet FROM cache
                WHERE query=? AND timestamp > ?
            """, (query, expiry_str))

        rows = cursor.fetchall()
        conn.close()
        return [{"title": r[0], "url": r[1], "snippet": r[2]} for r in rows]
