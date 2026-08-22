"""API v1 总路由 — 聚合所有子路由"""

from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.articles import router as articles_router
from app.api.v1.admin_articles import router as admin_articles_router
from app.api.v1.projects import router as projects_router
from app.api.v1.admin_projects import router as admin_projects_router
from app.api.v1.skills import router as skills_router
from app.api.v1.admin_skills import router as admin_skills_router
from app.api.v1.troubleshooting import router as troubleshooting_router
from app.api.v1.admin_troubleshooting import router as admin_troubleshooting_router
from app.api.v1.timeline import router as timeline_router
from app.api.v1.admin_timeline import router as admin_timeline_router
from app.api.v1.profile import router as profile_router
from app.api.v1.admin_profile import router as admin_profile_router

api_v1_router = APIRouter(prefix="/api/v1")

# ── 公开路由 ──
api_v1_router.include_router(auth_router)
api_v1_router.include_router(articles_router)
api_v1_router.include_router(projects_router)
api_v1_router.include_router(skills_router)
api_v1_router.include_router(troubleshooting_router)
api_v1_router.include_router(timeline_router)
api_v1_router.include_router(profile_router)

# ── 管理路由（需 JWT）──
api_v1_router.include_router(admin_articles_router)
api_v1_router.include_router(admin_projects_router)
api_v1_router.include_router(admin_skills_router)
api_v1_router.include_router(admin_troubleshooting_router)
api_v1_router.include_router(admin_timeline_router)
api_v1_router.include_router(admin_profile_router)

# ── 以下路由将在后续阶段添加 ──
# api_v1_router.include_router(upload_router)        # 阶段 7
