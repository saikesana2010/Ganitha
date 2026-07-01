import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch


# Patch DB so tests run without PostgreSQL
@pytest.fixture(autouse=True)
def mock_db(monkeypatch):
    monkeypatch.setattr("app.db.session.init_db", AsyncMock())
    monkeypatch.setattr("app.db.cache.get_cached", AsyncMock(return_value=None))
    monkeypatch.setattr("app.db.cache.save_to_cache", AsyncMock())


@pytest.fixture
def client():
    from app.main import app
    with TestClient(app) as c:
        yield c


class TestHomeEndpoint:
    def test_home(self, client):
        r = client.get("/")
        assert r.status_code == 200
        assert "Magine" in r.json()["message"]


class TestSolveEndpoint:
    def test_algebra(self, client):
        r = client.post("/solve", json={"question": "2x + 3 = 7"})
        assert r.status_code == 200
        data = r.json()
        assert data["type"] == "algebra"
        assert "2" in data["answer"]
        assert len(data["steps"]) > 0

    def test_geometry(self, client):
        r = client.post("/solve", json={"question": "area of circle radius 5"})
        assert r.status_code == 200
        data = r.json()
        assert data["type"] == "geometry"
        assert "78.5" in data["answer"]

    def test_arithmetic(self, client):
        r = client.post("/solve", json={"question": "25% of 200"})
        assert r.status_code == 200
        data = r.json()
        assert data["type"] == "arithmetic"
        assert "50" in data["answer"]

    def test_trig(self, client):
        r = client.post("/solve", json={"question": "sin 30 degrees"})
        assert r.status_code == 200
        data = r.json()
        assert data["type"] == "trigonometry"

    def test_empty_question(self, client):
        r = client.post("/solve", json={"question": ""})
        assert r.status_code in (200, 422)

    def test_missing_field(self, client):
        r = client.post("/solve", json={})
        assert r.status_code == 422
