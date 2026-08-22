"""技能公开路由（无需认证）"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.skill import SkillGroupResponse
from app.services import skill as skill_service
from app.utils.response import list_response

router = APIRouter(prefix="/skills", tags=["技能（公开）"])


@router.get("")
def get_skills(db: Session = Depends(get_db)):
    """获取所有技能组（含技能项，嵌套结构）"""
    groups = skill_service.get_skill_groups_with_items(db)
    total = len(groups)
    data = [SkillGroupResponse.model_validate(g).model_dump(mode="json", by_alias=True) for g in groups]
    return list_response(data=data, total=total)
