"""FastAPI entrypoint for the Cars CRUD app.

提供：
- GET  /                  -> 单页 HTML 界面
- /static/*              -> 静态资源（CSS / JS）
- REST CRUD API on /api/cars

服务端绑定 0.0.0.0:8000（由 Dockerfile 的 CMD 启动），
因此容器发布的端口可以访问到应用。
"""
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

import app.database as db

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Cars CRUD", version="1.0.0")


class CarCreate(BaseModel):
    make: str = Field(..., min_length=1, max_length=50)
    model: str = Field(..., min_length=1, max_length=50)
    year: int | None = Field(default=None, ge=1886, le=2100)
    color: str | None = Field(default=None, max_length=30)


class CarOut(BaseModel):
    id: int
    make: str
    model: str
    year: int | None = None
    color: str | None = None


@app.on_event("startup")
def _startup():
    db.init_db()


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/api/cars", response_model=list[CarOut])
def list_cars():
    return db.list_cars()


@app.post("/api/cars", response_model=CarOut, status_code=201)
def create_car(car: CarCreate):
    return db.create_car(car.model_dump())


@app.get("/api/cars/{car_id}", response_model=CarOut)
def get_car(car_id: int):
    car = db.get_car(car_id)
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


@app.put("/api/cars/{car_id}", response_model=CarOut)
def update_car(car_id: int, car: CarCreate):
    updated = db.update_car(car_id, car.model_dump())
    if updated is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return updated


@app.delete("/api/cars/{car_id}", status_code=204)
def delete_car(car_id: int):
    if not db.delete_car(car_id):
        raise HTTPException(status_code=404, detail="Car not found")


app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
