import sqlite3
from datetime import datetime, timedelta

class Cache:
    """
    Gestion d'un cache SQLite avec TTL pour éviter de rescraper.
    Chaque entrée a : source, query, url, title, snippet et timestamp.
    """

    def __init__(self, db_path="cache.db", ttl_seconds=86400):
        self.db_path = db_path
        self.ttl_seconds = ttl_seconds
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

    def save(self, source, query, results):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        for item in results:
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
        if source:
            cursor.execute("SELECT title, url, snippet, timestamp FROM cache WHERE query=? AND source=?", (query, source))
        else:
            cursor.execute("SELECT title, url, snippet, timestamp FROM cache WHERE query=?", (query,))
        rows = cursor.fetchall()
        conn.close()

        valid_results = []
        now = datetime.now()
        for title, url, snippet, ts in rows:
            timestamp = datetime.fromisoformat(ts) if isinstance(ts, str) else ts
            if now - timestamp <= timedelta(seconds=self.ttl_seconds):
                valid_results.append({"title": title, "url": url, "snippet": snippet})
        return valid_results
