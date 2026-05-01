import os
os.environ.update(
    PGHOST="localhost", PGPORT="5432", PGUSER="test",
    PGPASSWORD="test", PGDATABASE="test", JWT_SECRET="test-secret-key",
)

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.db import Base, get_db
from app.main import app

test_engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
TestSession = sessionmaker(bind=test_engine, autocommit=False, autoflush=False)

for tbl in Base.metadata.tables.values():
    tbl.schema = None


def _test_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = _test_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_header(client):
    creds = {"username": "testuser", "password": "pass1234"}
    client.post("/api/users/register", json=creds)
    resp = client.post("/api/users/login", json=creds)
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}
