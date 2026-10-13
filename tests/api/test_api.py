"""API 测试：通过 FastAPI TestClient 验证 REST 端点。"""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client(car_db):
    with TestClient(app) as c:
        yield c


def test_list_empty(client):
    r = client.get("/api/cars")
    assert r.status_code == 200
    assert r.json() == []


def test_create_returns_201(client):
    r = client.post("/api/cars", json={"make": "BMW", "model": "X5", "year": 2021, "color": "Silver"})
    assert r.status_code == 201
    body = r.json()
    assert body["make"] == "BMW"
    assert body["id"] > 0


def test_get_missing_returns_404(client):
    assert client.get("/api/cars/99999").status_code == 404


def test_create_rejects_invalid(client):
    assert client.post("/api/cars", json={"model": "X5"}).status_code == 422


def test_update_and_delete_flow(client):
    created = client.post("/api/cars", json={"make": "Audi", "model": "A4", "year": 2018, "color": "Grey"}).json()
    up = client.put(f"/api/cars/{created['id']}", json={"make": "Audi", "model": "A4", "year": 2019, "color": "Black"})
    assert up.status_code == 200
    assert up.json()["year"] == 2019
    assert up.json()["color"] == "Black"

    assert client.delete(f"/api/cars/{created['id']}").status_code == 204
    assert client.get(f"/api/cars/{created['id']}").status_code == 404
