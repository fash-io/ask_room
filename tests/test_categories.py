# tests/test_categories.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.database import Base, engine, SessionLocal
from app.database import get_db

# Create a fresh database for testing
@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture()
def client(db_session: Session):
    def override_get_db():
        yield db_session
    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


def test_create_category(client):
    response = client.post(
        "/api/categories/", json={"name": "TestCat", "description": "Desc"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "TestCat"
    assert data["description"] == "Desc"


def test_get_categories(client):
    client.post("/api/categories/", json={"name": "Cat2", "description": "Desc2"})
    response = client.get("/api/categories/")
    assert response.status_code == 200
    cats = response.json()
    assert isinstance(cats, list)
    assert any(c["name"] == "Cat2" for c in cats)

