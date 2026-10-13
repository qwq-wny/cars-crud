"""集成测试：直接验证 SQLite 存储层的 CRUD 函数。"""


def test_create_and_get(car_db):
    created = car_db.create_car({"make": "Honda", "model": "Civic", "year": 2019, "color": "Blue"})
    assert created["id"] > 0
    got = car_db.get_car(created["id"])
    assert got["make"] == "Honda"
    assert got["model"] == "Civic"


def test_update_existing(car_db):
    c = car_db.create_car({"make": "Ford", "model": "Focus", "year": 2015, "color": None})
    updated = car_db.update_car(c["id"], {"make": "Ford", "model": "Focus", "year": 2018, "color": "White"})
    assert updated["year"] == 2018
    assert updated["color"] == "White"


def test_update_missing_returns_none(car_db):
    assert car_db.update_car(99999, {"make": "X", "model": "Y", "year": None, "color": None}) is None


def test_delete_existing(car_db):
    c = car_db.create_car({"make": "Tesla", "model": "Model 3", "year": 2022, "color": "Black"})
    assert car_db.delete_car(c["id"]) is True
    assert car_db.get_car(c["id"]) is None


def test_delete_missing_returns_false(car_db):
    assert car_db.delete_car(99999) is False


def test_list_returns_all_in_order(car_db):
    car_db.create_car({"make": "A", "model": "B", "year": 2000, "color": None})
    car_db.create_car({"make": "C", "model": "D", "year": 2001, "color": "Green"})
    cars = car_db.list_cars()
    assert len(cars) == 2
    assert cars[0]["make"] == "A"
    assert cars[1]["make"] == "C"
