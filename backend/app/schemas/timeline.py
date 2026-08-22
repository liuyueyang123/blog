"""时间线 Pydantic v2 Schemas

注意：数据库列名为 time_label（避免 MySQL 保留字 time），
前端字段为 time，这里做映射。
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class TimelineItemCreate(BaseModel):
    time: str = Field(default="", max_length=100)
    title: str = Field(..., min_length=1, max_length=300)
    detail: str = Field(default="")
    sort_order: int = 0


class TimelineItemUpdate(BaseModel):
    time: Optional[str] = Field(None, max_length=100)
    title: Optional[str] = Field(None, min_length=1, max_length=300)
    detail: Optional[str] = None
    sort_order: Optional[int] = None


class TimelineItemResponse(BaseModel):
    """与前端 TimelineItem 接口对齐：time, title, detail"""
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    # ORM 属性 time_label → 响应字段 time
    time: str = Field(validation_alias="time_label")
    title: str
    detail: str

    id: Optional[int] = None
    sort_order: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
