import pytest
from unittest.mock import patch
from app import database

@pytest.fixture(autouse=True)
def isolate_test_database(tmp_path):
    """Ensure every test runs against an isolated, temporary scratch database.
    Prevents tests from ever touching data/movie_excluder.db.
    """
    test_db = tmp_path / "test_scratch.db"
    with patch.object(database, "DATABASE_PATH", test_db):
        database.initialize_database()
        yield
