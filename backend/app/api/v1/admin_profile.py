"""个人资料管理路由（需要 JWT 认证）"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.api.deps import get_current_admin
from app.models.admin import Admin
from app.schemas.profile import ProfileUpdate
from app.services import profile as profile_service
from app.utils.response import success

router = APIRouter(prefix="/admin/profile", tags=["个人资料管理"])


@router.get("")
def get_profile(
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    """获取个人资料"""
    profile = profile_service.get_or_create_profile(db)
    resp = profile_service.profile_to_response(profile)
    return success(data=resp.model_dump(mode="json", by_alias=True))


@router.put("")
def update_profile(
    body: ProfileUpdate,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    """更新个人资料（含社交链接和能力卡片）"""
    profile = profile_service.get_or_create_profile(db)
    updated = profile_service.update_profile(db, profile, body)
    resp = profile_service.profile_to_response(updated)
    return success(data=resp.model_dump(mode="json", by_alias=True), message="Profile updated")
