"""个人资料公开路由（无需认证）"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.services import profile as profile_service
from app.utils.response import success

router = APIRouter(prefix="/profile", tags=["个人资料（公开）"])


@router.get("")
def get_profile(db: Session = Depends(get_db)):
    """
    获取个人资料（含 socialLinks + capabilityCards 嵌套结构）。
    若数据库中还没有资料行，自动创建空行并返回。
    """
    profile = profile_service.get_or_create_profile(db)
    resp = profile_service.profile_to_response(profile)
    return success(data=resp.model_dump(mode="json", by_alias=True))
