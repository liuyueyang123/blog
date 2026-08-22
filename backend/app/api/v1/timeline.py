"""时间线公开路由（无需认证）"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.timeline import TimelineItemResponse
from app.services import timeline as timeline_service
from app.utils.response import list_response

router = APIRouter(prefix="/timeline", tags=["时间线（公开）"])


@router.get("")
def get_timeline(db: Session = Depends(get_db)):
    """获取时间线列表"""
    items = timeline_service.get_timeline_items(db)
    total = len(items)
    data = [TimelineItemResponse.model_validate(i).model_dump(mode="json", by_alias=True) for i in items]
    return list_response(data=data, total=total)
