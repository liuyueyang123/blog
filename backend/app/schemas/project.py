"""项目 Pydantic v2 Schemas"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


# ── 请求 ──────────────────────────────────────────────────

class ProjectCreate(BaseModel):
    slug: str = Field(..., min_length=1, max_length=200)
    title: str = Field(..., min_length=1, max_length=300)
    subtitle: str = Field(default="", max_length=500)
    cover_tone: str = Field(default="default", max_length=50)
    tags: List[str] = Field(default_factory=list)
    role: str = Field(default="")
    result: str = Field(default="")
    overview: str = Field(default="")
    highlights: List[str] = Field(default_factory=list)
    github_url: str = Field(default="", max_length=500)
    is_published: bool = True
    sort_order: int = 0


class ProjectUpdate(BaseModel):
    """所有字段可选，只更新传入的字段"""
    slug: Optional[str] = Field(None, min_length=1, max_length=200)
    title: Optional[str] = Field(None, min_length=1, max_length=300)
    subtitle: Optional[str] = Field(None, max_length=500)
    cover_tone: Optional[str] = Field(None, max_length=50)
    tags: Optional[List[str]] = None
    role: Optional[str] = None
    result: Optional[str] = None
    overview: Optional[str] = None
    highlights: Optional[List[str]] = None
    github_url: Optional[str] = Field(None, max_length=500)
    is_published: Optional[bool] = None
    sort_order: Optional[int] = None


# ── 响应 ──────────────────────────────────────────────────

class ProjectResponse(BaseModel):
    """
    与前端 Project 接口对齐（camelCase）。
    前端类型：slug, title, subtitle, coverTone, tags, role, result,
             overview, highlights, githubUrl
    """
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )

    slug: str
    title: str
    subtitle: str
    cover_tone: str
    tags: List[str]
    role: str
    result: str
    overview: str
    highlights: List[str]
    github_url: str

    # 管理接口额外字段
    id: Optional[int] = None
    is_published: Optional[bool] = None
    sort_order: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
