"""故障排查案例 Pydantic v2 Schemas"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class TroubleshootingCaseCreate(BaseModel):
    slug: str = Field(..., min_length=1, max_length=200)
    title: str = Field(..., min_length=1, max_length=300)
    symptom: str = Field(default="")
    process: str = Field(default="")
    tools: List[str] = Field(default_factory=list)
    root_cause: str = Field(default="")
    resolution: str = Field(default="")
    review: str = Field(default="")
    is_published: bool = True
    sort_order: int = 0


class TroubleshootingCaseUpdate(BaseModel):
    slug: Optional[str] = Field(None, min_length=1, max_length=200)
    title: Optional[str] = Field(None, min_length=1, max_length=300)
    symptom: Optional[str] = None
    process: Optional[str] = None
    tools: Optional[List[str]] = None
    root_cause: Optional[str] = None
    resolution: Optional[str] = None
    review: Optional[str] = None
    is_published: Optional[bool] = None
    sort_order: Optional[int] = None


class TroubleshootingCaseResponse(BaseModel):
    """
    与前端 TroubleshootingCase 接口对齐：
    slug, title, symptom, process, tools, rootCause, resolution, review
    """
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )

    slug: str
    title: str
    symptom: str
    process: str
    tools: List[str]
    root_cause: str
    resolution: str
    review: str

    id: Optional[int] = None
    is_published: Optional[bool] = None
    sort_order: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
