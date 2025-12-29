import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.models as _models  # noqa: F401

# Shared test configuration: environment and imports used by
# both unit and integration tests
os.environ.setdefault("JWT_SECRET", "test-secret-abcdefghijklmnopqrstuvwxyz-123456")
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")

from unittest.mock import Mock

from app.db.session import (
    Base,  # ← SPRÁVNÝ IMPORT
    get_db,
)
from app.main import app

# Shared fixtures for module-based test organization
# Integration-marked tests will use the `db` fixture below; unit tests use `mock_db`.


@pytest.fixture(scope="function")
def db(tmp_path):
    """Integration DB fixture: creates an isolated SQLite file-based DB per test."""
    db_file = tmp_path / "test.db"
    engine = create_engine(
        f"sqlite:///{db_file}", connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(bind=engine)

    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def mock_db():
    """Provide a mock DB session usable by unit tests (overrides `get_db`)."""
    mock = Mock()
    # Default: queries return no results unless a test configures the mock explicitly
    mock.query.return_value.filter.return_value.first.return_value = None

    def override_get_db_mock():
        yield mock

    app.dependency_overrides[get_db] = override_get_db_mock
    try:
        yield mock
    finally:
        app.dependency_overrides.pop(get_db, None)


@pytest.fixture(scope="function")
def client(request):
    """Universal TestClient.

    Uses `mock_db` by default, and switches to `db` for tests marked
    `integration`.

    """
    marker = request.node.get_closest_marker("integration")

    if marker:
        db = request.getfixturevalue("db")

        def override_get_db():
            yield db

        app.dependency_overrides[get_db] = override_get_db
        try:
            with TestClient(app) as c:
                yield c
        finally:
            app.dependency_overrides.pop(get_db, None)
    else:
        mock = request.getfixturevalue("mock_db")

        def override_get_db():
            yield mock

        app.dependency_overrides[get_db] = override_get_db
        try:
            with TestClient(app) as c:
                yield c
        finally:
            app.dependency_overrides.pop(get_db, None)
