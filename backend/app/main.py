"""FastAPI 应用入口"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.api.v1.router import api_v1_router
from app.utils.response import success

settings = get_settings()

# 生产环境关闭 Swagger/ReDoc/OpenAPI 文档，避免暴露接口结构
_is_prod = settings.app_env == "production"

app = FastAPI(
    title="Yael Portfolio Blog API",
    description="技术作品集 + 博客后端 API",
    version="0.1.0",
    docs_url=None if _is_prod else "/api/docs",
    redoc_url=None if _is_prod else "/api/redoc",
    openapi_url=None if _is_prod else "/api/openapi.json",
)

# ── CORS ──────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── 路由挂载 ──────────────────────────────────────────────
app.include_router(api_v1_router)


# ── 静态文件：上传的图片 ──────────────────────────────────
# 开发环境由后端直接 serve；生产环境由 Nginx 直接映射到同一目录
_upload_dir = Path(settings.upload_dir).resolve()
_upload_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(_upload_dir)), name="uploads")


# ── 健康检查 ──────────────────────────────────────────────
@app.get("/api/health", tags=["系统"])
def health_check():
    return success(message="ok")
