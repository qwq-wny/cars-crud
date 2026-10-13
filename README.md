# Cars CRUD

FastAPI + plain HTML + SQLite 的车辆管理示例应用，配套 Docker 容器化与 GitHub Actions 自动发布流程。

## 本地运行

```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000/ ，API 文档在 http://localhost:8000/docs 。

## Docker

```bash
# 构建（Docker Hub 慢时可加 --build-arg BASE_IMAGE=efreiwut.azurecr.io/dockerhub/library/python:3.12-slim）
docker build -t cars-crud:local .

# 运行（SQLite 数据保存在命名卷 cars-data 中）
docker run -d --name cars-app -p 127.0.0.1:8000:8000 \
  --mount type=volume,source=cars-data,target=/data cars-crud:local
```

## 测试

```bash
pip install -r requirements.txt pytest httpx
pytest tests/unit/ tests/integration/ tests/api/ tests/e2e/
```

## CI/CD

`.github/workflows/tests.yml`：
- **PR 指向 main**：只运行 unit / integration / api / e2e 四组测试，不发布镜像。
- **push 到 main**：测试全部通过后，用 Docker Buildx 构建并推送到 Docker Hub（`<DOCKERHUB_USERNAME>/cars-crud:latest` + commit SHA 标签）。

发布需要仓库配置两个 secrets：

| Secret | 值 |
|---|---|
| `DOCKERHUB_USERNAME` | Docker Hub 用户名 |
| `DOCKERHUB_TOKEN` | Docker Hub Personal Access Token（Repo Read & Write） |
