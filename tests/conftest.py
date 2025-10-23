import builtins
import sqlite3
from unittest.mock import MagicMock, patch

import pytest

from core.cache import Cache


# ------------------------------
# FIXTURE: Cache mocké
# ------------------------------
@pytest.fixture
def mock_cache():
    cache_instance = MagicMock(spec=Cache)
    cache_instance.load.return_value = []
    cache_instance.save.return_value = None
    return cache_instance

# ------------------------------
# FIXTURE: SQLite DB mockée
# ------------------------------
@pytest.fixture
def mock_sqlite(monkeypatch):
    class MockCursor:
        def execute(self, *args, **kwargs): return None
        def fetchall(self): return []
        def close(self): return None
    class MockConnection:
        def cursor(self): return MockCursor()
        def commit(self): return None
        def close(self): return None

    monkeypatch.setattr(sqlite3, "connect", lambda *a, **kw: MockConnection())
    return MockConnection()

# ------------------------------
# FIXTURE: Mock requests.get
# ------------------------------
@pytest.fixture
def mock_requests(monkeypatch):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "<html></html>"
    mock_response.json.return_value = {"items": []}

    def mock_get(*args, **kwargs):
        return mock_response

    monkeypatch.setattr("requests.get", mock_get)
    return mock_response

# ------------------------------
# FIXTURE: Open mock pour sauvegarde fichiers
# ------------------------------
@pytest.fixture
def mock_open(monkeypatch):
    m_open = MagicMock()
    monkeypatch.setattr(builtins, "open", m_open)
    return m_open

# ------------------------------
# FIXTURE: Logger mocké pour tests
# ------------------------------
@pytest.fixture
def mock_logger(monkeypatch):
    class MockLogger:
        def info(self, *args, **kwargs): pass
        def error(self, *args, **kwargs): pass
        def warning(self, *args, **kwargs): pass

    monkeypatch.setattr("core.utils.setup_logger", lambda *a, **kw: MockLogger())
    return MockLogger()
