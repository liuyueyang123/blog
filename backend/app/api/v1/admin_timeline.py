"""时间线管理路由（需要 JWT 认证）"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.api.deps import get_current_admin
from app.models.admin import Admin
from app.schemas.timeline import TimelineItemCreate, TimelineItemUpdate, TimelineItemResponse
from app.services import timeline as timeline_service
from app.utils.response import success, list_response

router = APIRouter(prefix="/admin/timeline", tags=["时间线管理"])


@router.get("")
def get_all_items(
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    """获取所有时间线项"""
    items = timeline_service.get_timeline_items(db)
    total = len(items)
    data = [TimelineItemResponse.model_validate(i).model_dump(mode="json", by_alias=True) for i in items]
    return list_response(data=data, total=total)


@router.post("")
def create_item(
    body: TimelineItemCreate,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    """新增时间线项"""
    item = timeline_service.create_timeline_item(db, body)
    return success(
        data=TimelineItemResponse.model_validate(item).model_dump(mode="json", by_alias=True),
        message="Timeline item created",
    )


@router.put("/{item_id}")
def update_item(
    item_id: int,
    body: TimelineItemUpdate,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    """更新时间线项"""
    item = timeline_service.get_timeline_item_by_id(db, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timeline item not found")
    updated = timeline_service.update_timeline_item(db, item, body)
    return success(
        data=TimelineItemResponse.model_validate(updated).model_dump(mode="json", by_alias=True),
        message="Timeline item updated",
    )


@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    """删除时间线项"""
    item = timeline_service.get_timeline_item_by_id(db, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timeline item not found")
    timeline_service.delete_timeline_item(db, item)
    return success(message="Timeline item deleted")
