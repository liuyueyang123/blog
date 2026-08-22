"""技能 Pydantic v2 Schemas（技能组 + 技能项嵌套）"""

from datetime import datetime
from typing import List, Optional, Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

# 与前端 Status 联合类型一致的 4 级状态
SkillStatus = Literal[
    "有项目实践",
    "能够独立完成基础操作",
    "能够排查常见问题",
    "正在系统学习",
]


# ── 技能项 ────────────────────────────────────────────────

class SkillItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    direction: str = Field(default="", max_length=200)
    scenario: str = Field(default="")
    status: SkillStatus = "正在系统学习"
    sort_order: int = 0


class SkillItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    direction: Optional[str] = Field(None, max_length=200)
    scenario: Optional[str] = None
    status: Optional[SkillStatus] = None
    sort_order: Optional[int] = None


class SkillItemResponse(BaseModel):
    """与前端 SkillItem 接口对齐：name, direction, scenario, status"""
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )

    name: str
    direction: str
    scenario: str
    status: str

    id: Optional[int] = None
    group_id: Optional[int] = None
    sort_order: Optional[int] = None


# ── 技能组 ────────────────────────────────────────────────

class SkillGroupCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    summary: str = Field(default="", max_length=500)
    sort_order: int = 0


class SkillGroupUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    summary: Optional[str] = Field(None, max_length=500)
    sort_order: Optional[int] = None


class SkillGroupResponse(BaseModel):
    """与前端 SkillGroup 接口对齐：title, summary, items[]"""
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )

    title: str
    summary: str
    items: List[SkillItemResponse] = []

    id: Optional[int] = None
    sort_order: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
