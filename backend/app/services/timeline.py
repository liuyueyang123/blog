"""时间线服务层

注意：schema 字段 time ↔ 数据库列 time_label 的映射在此处理。
"""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.timeline import TimelineItem
from app.schemas.timeline import TimelineItemCreate, TimelineItemUpdate


def get_timeline_items(db: Session) -> List[TimelineItem]:
    """获取所有时间线项（按 sort_order 排序）"""
    stmt = select(TimelineItem).order_by(
        TimelineItem.sort_order.asc(), TimelineItem.id.asc()
    )
    return list(db.execute(stmt).scalars().all())


def get_timeline_item_by_id(db: Session, item_id: int) -> Optional[TimelineItem]:
    """根据 ID 获取时间线项"""
    return db.get(TimelineItem, item_id)


def create_timeline_item(db: Session, data: TimelineItemCreate) -> TimelineItem:
    """创建时间线项（time → time_label 映射）"""
    payload = data.model_dump()
    payload["time_label"] = payload.pop("time")
    item = TimelineItem(**payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_timeline_item(db: Session, item: TimelineItem, data: TimelineItemUpdate) -> TimelineItem:
    """更新时间线项"""
    update_data = data.model_dump(exclude_unset=True)
    if "time" in update_data:
        update_data["time_label"] = update_data.pop("time")
    for field, value in update_data.items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


def delete_timeline_item(db: Session, item: TimelineItem) -> None:
    """删除时间线项"""
    db.delete(item)
    db.commit()
