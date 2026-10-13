"""共享 fixtures：让测试使用隔离的临时 SQLite 数据库。

通过直接修改 app.database.DB_PATH（而非 reload），
main.py 中 `import app.database as db` 与这里引用同一模块对象，
因此应用端点也会读到新的数据库路径。
"""
import app.database as db
import pytest


@pytest.fixture
def car_db(tmp_path):
    db.DB_PATH = str(tmp_path / "test.db")
    db.init_db()
    yield db
