"""文章 Pydantic v2 Schemas"""

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


# ── 请求 ──────────────────────────────────────────────────

class ArticleCreate(BaseModel):
    slug: str = Field(..., min_length=1, max_length=200)
    title: str = Field(..., min_length=1, max_length=300)
    category: str = Field(default="", max_length=100)
    excerpt: str = Field(default="")
    date: date
    read_time: str = Field(default="5 min", max_length=50)
    content: List[str] = Field(default_factory=list)
    is_published: bool = True
    sort_order: int = 0


class ArticleUpdate(BaseModel):
    """所有字段可选，只更新传入的字段"""
    slug: Optional[str] = Field(None, min_length=1, max_length=200)
    title: Optional[str] = Field(None, min_length=1, max_length=300)
    category: Optional[str] = Field(None, max_length=100)
    excerpt: Optional[str] = None
    date: Optional[date] = None
    read_time: Optional[str] = Field(None, max_length=50)
    content: Optional[List[str]] = None
    is_published: Optional[bool] = None
    sort_order: Optional[int] = None


# ── 响应 ──────────────────────────────────────────────────

class ArticleResponse(BaseModel):
    """
    与前端 Article 接口对齐（camelCase）。
    前端类型：slug, title, category, excerpt, date, readTime, content
    使用 alias_generator=to_camel 自动将 snake_case → camelCase 输出。
    """
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )

    slug: str
    title: str
    category: str
    excerpt: str
    date: date
    read_time: str
    content: List[str]

    # 管理接口额外字段
    id: Optional[int] = None
    is_published: Optional[bool] = None
    sort_order: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
