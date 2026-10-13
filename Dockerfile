# 基础镜像可通过构建参数切换：本地若访问 Docker Hub 慢，可用 Azure 代理
ARG BASE_IMAGE=python:3.12-slim
FROM ${BASE_IMAGE}

WORKDIR /app

# 先拷贝依赖清单并安装，便于 Docker 复用依赖层（改代码时不必重装依赖）
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

# 拷贝应用代码（app/ 含 FastAPI 入口 + 前端静态文件）
COPY app/ ./app/

# 创建 SQLite 数据目录并交给非特权用户 10001，避免容器内写权限问题
RUN mkdir -p /data && chown 10001:10001 /data
USER 10001:10001

# 数据库文件写入命名卷挂载点 /data
ENV CARS_DB_PATH=/data/cars.db

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
