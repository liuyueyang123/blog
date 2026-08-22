"""技能服务层：技能组 + 技能项 CRUD"""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.skill import SkillGroup, SkillItem
from app.schemas.skill import (
    SkillGroupCreate,
    SkillGroupUpdate,
    SkillItemCreate,
    SkillItemUpdate,
)


# ── 技能组 ────────────────────────────────────────────────

def get_skill_groups_with_items(db: Session) -> List[SkillGroup]:
    """获取所有技能组（含技能项，按 sort_order 排序）"""
    stmt = (
        select(SkillGroup)
        .options(selectinload(SkillGroup.items))
        .order_by(SkillGroup.sort_order.asc(), SkillGroup.id.asc())
    )
    return list(db.execute(stmt).scalars().all())


def get_skill_group_by_id(db: Session, group_id: int) -> Optional[SkillGroup]:
    """根据 ID 获取技能组（含技能项）"""
    stmt = (
        select(SkillGroup)
        .options(selectinload(SkillGroup.items))
        .where(SkillGroup.id == group_id)
    )
    return db.execute(stmt).scalar_one_or_none()


def create_skill_group(db: Session, data: SkillGroupCreate) -> SkillGroup:
    """创建技能组"""
    group = SkillGroup(**data.model_dump())
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


def update_skill_group(db: Session, group: SkillGroup, data: SkillGroupUpdate) -> SkillGroup:
    """更新技能组"""
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(group, field, value)
    db.commit()
    db.refresh(group)
    return group


def delete_skill_group(db: Session, group: SkillGroup) -> None:
    """删除技能组（级联删除技能项）"""
    db.delete(group)
    db.commit()


# ── 技能项 ────────────────────────────────────────────────

def get_skill_item_by_id(db: Session, item_id: int) -> Optional[SkillItem]:
    """根据 ID 获取技能项"""
    return db.get(SkillItem, item_id)


def create_skill_item(db: Session, group_id: int, data: SkillItemCreate) -> SkillItem:
    """在指定技能组下创建技能项"""
    item = SkillItem(group_id=group_id, **data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_skill_item(db: Session, item: SkillItem, data: SkillItemUpdate) -> SkillItem:
    """更新技能项"""
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


def delete_skill_item(db: Session, item: SkillItem) -> None:
    """删除技能项"""
    db.delete(item)
    db.commit()
