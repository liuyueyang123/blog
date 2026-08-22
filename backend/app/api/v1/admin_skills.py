"""技能管理路由（需要 JWT 认证）：技能组 CRUD + 技能项 CRUD"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.api.deps import get_current_admin
from app.models.admin import Admin
from app.schemas.skill import (
    SkillGroupCreate,
    SkillGroupUpdate,
    SkillGroupResponse,
    SkillItemCreate,
    SkillItemUpdate,
    SkillItemResponse,
)
from app.services import skill as skill_service
from app.utils.response import success, list_response

router = APIRouter(prefix="/admin", tags=["技能管理"])


# ── 技能组 ────────────────────────────────────────────────

@router.get("/skills")
def get_all_skill_groups(
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    """获取所有技能组（含技能项）"""
    groups = skill_service.get_skill_groups_with_items(db)
    total = len(groups)
    data = [SkillGroupResponse.model_validate(g).model_dump(mode="json", by_alias=True) for g in groups]
    return list_response(data=data, total=total)


@router.post("/skill-groups")
def create_skill_group(
    body: SkillGroupCreate,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    """新增技能组"""
    group = skill_service.create_skill_group(db, body)
    return success(
        data=SkillGroupResponse.model_validate(group).model_dump(mode="json", by_alias=True),
        message="Skill group created",
    )


@router.put("/skill-groups/{group_id}")
def update_skill_group(
    group_id: int,
    body: SkillGroupUpdate,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    """更新技能组"""
    group = skill_service.get_skill_group_by_id(db, group_id)
    if group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill group not found")
    updated = skill_service.update_skill_group(db, group, body)
    return success(
        data=SkillGroupResponse.model_validate(updated).model_dump(mode="json", by_alias=True),
        message="Skill group updated",
    )


@router.delete("/skill-groups/{group_id}")
def delete_skill_group(
    group_id: int,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    """删除技能组（级联删除技能项）"""
    group = skill_service.get_skill_group_by_id(db, group_id)
    if group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill group not found")
    skill_service.delete_skill_group(db, group)
    return success(message="Skill group deleted")


# ── 技能项 ────────────────────────────────────────────────

@router.post("/skill-groups/{group_id}/items")
def create_skill_item(
    group_id: int,
    body: SkillItemCreate,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    """在指定技能组下新增技能项"""
    group = skill_service.get_skill_group_by_id(db, group_id)
    if group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill group not found")
    item = skill_service.create_skill_item(db, group_id, body)
    return success(
        data=SkillItemResponse.model_validate(item).model_dump(mode="json", by_alias=True),
        message="Skill item created",
    )


@router.put("/skill-items/{item_id}")
def update_skill_item(
    item_id: int,
    body: SkillItemUpdate,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    """更新技能项"""
    item = skill_service.get_skill_item_by_id(db, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill item not found")
    updated = skill_service.update_skill_item(db, item, body)
    return success(
        data=SkillItemResponse.model_validate(updated).model_dump(mode="json", by_alias=True),
        message="Skill item updated",
    )


@router.delete("/skill-items/{item_id}")
def delete_skill_item(
    item_id: int,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    """删除技能项"""
    item = skill_service.get_skill_item_by_id(db, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill item not found")
    skill_service.delete_skill_item(db, item)
    return success(message="Skill item deleted")
