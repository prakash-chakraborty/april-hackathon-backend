import os
os.environ["PGHOST"] = "localhost"
os.environ["PGPORT"] = "5432"
os.environ["PGUSER"] = "test"
os.environ["PGPASSWORD"] = "test"
os.environ["PGDATABASE"] = "test"
os.environ["JWT_SECRET"] = "test-secret-key"

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.db import Base, get_db
from app.main import app

# use sqlite for tests so we dont need a real pg instance
engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_test_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = get_test_db


@pytest.fixture(autouse=True)
def reset_tables():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_header(client):
    # register + login to get a token we can use in other tests
    client.post("/api/users/register", json={"username": "testuser", "password": "pass1234"})
    resp = client.post("/api/users/login", json={"username": "testuser", "password": "pass1234"})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
