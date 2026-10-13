"""SQLite 存储层 for the Cars CRUD app.

数据库文件位置由环境变量 CARS_DB_PATH 控制，默认放在本模块旁。
容器内运行时 Dockerfile 会把该路径指向 /data/cars.db（命名卷）。
"""
import os
import sqlite3

DB_PATH = os.environ.get(
    "CARS_DB_PATH",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "cars.db"),
)


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """确保 cars 表存在（幂等）。"""
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cars (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                make  TEXT NOT NULL,
                model TEXT NOT NULL,
                year  INTEGER,
                color TEXT
            )
            """
        )


def _row_to_dict(row):
    return {key: row[key] for key in row.keys()}


def list_cars():
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM cars ORDER BY id").fetchall()
    return [_row_to_dict(r) for r in rows]


def get_car(car_id):
    with _connect() as conn:
        row = conn.execute("SELECT * FROM cars WHERE id = ?", (car_id,)).fetchone()
    return _row_to_dict(row) if row else None


def create_car(data):
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO cars (make, model, year, color) VALUES (?, ?, ?, ?)",
            (data["make"], data["model"], data.get("year"), data.get("color")),
        )
        car_id = cur.lastrowid
    return get_car(car_id)


def update_car(car_id, data):
    with _connect() as conn:
        cur = conn.execute(
            "UPDATE cars SET make = ?, model = ?, year = ?, color = ? WHERE id = ?",
            (data["make"], data["model"], data.get("year"), data.get("color"), car_id),
        )
        changed = cur.rowcount > 0
    if not changed:
        return None
    return get_car(car_id)


def delete_car(car_id):
    with _connect() as conn:
        cur = conn.execute("DELETE FROM cars WHERE id = ?", (car_id,))
    return cur.rowcount > 0
