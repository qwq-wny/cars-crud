"""E2E 测试：模拟用户在浏览器里完成的完整流程，并验证页面/静态资源可访问。"""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client(car_db):
    with TestClient(app) as c:
        yield c


def test_index_page_renders(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "Cars CRUD" in r.text
    assert 'id="car-form"' in r.text
    assert 'id="cars-tbody"' in r.text


def test_static_assets_are_served(client):
    assert client.get("/static/app.js").status_code == 200
    assert client.get("/static/style.css").status_code == 200


def test_full_crud_user_flow(client):
    # 1) 从空列表开始
    assert client.get("/api/cars").json() == []

    # 2) 通过 HTML 表单对应的 POST 创建一辆车
    r = client.post("/api/cars", json={"make": "Volvo", "model": "XC60", "year": 2020, "color": "White"})
    assert r.status_code == 201
    car_id = r.json()["id"]

    # 3) 列表中出现该车
    ids = [c["id"] for c in client.get("/api/cars").json()]
    assert car_id in ids

    # 4) 编辑保存（PUT）
    up = client.put(f"/api/cars/{car_id}", json={"make": "Volvo", "model": "XC90", "year": 2021, "color": "Black"})
    assert up.json()["model"] == "XC90"

    # 5) 删除后列表清空
    assert client.delete(f"/api/cars/{car_id}").status_code == 204
    assert client.get("/api/cars").json() == []
