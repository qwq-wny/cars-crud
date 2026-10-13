"""单元测试：Pydantic 请求模型的字段校验逻辑。"""
import pytest
from pydantic import ValidationError

from app.main import CarCreate


def test_valid_car_model():
    car = CarCreate(make="Toyota", model="Corolla", year=2020, color="Red")
    assert car.make == "Toyota"
    assert car.model == "Corolla"
    assert car.year == 2020
    assert car.color == "Red"


def test_optional_fields_default_to_none():
    car = CarCreate(make="Honda", model="Civic")
    assert car.year is None
    assert car.color is None


def test_missing_required_field_rejected():
    with pytest.raises(ValidationError):
        CarCreate(model="Corolla")  # 缺少 make


def test_empty_make_rejected():
    with pytest.raises(ValidationError):
        CarCreate(make="", model="Corolla")


def test_year_out_of_range_rejected():
    with pytest.raises(ValidationError):
        CarCreate(make="Toyota", model="Corolla", year=1800)
    with pytest.raises(ValidationError):
        CarCreate(make="Toyota", model="Corolla", year=2200)
