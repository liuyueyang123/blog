"""个人资料 Pydantic v2 Schemas

Profile 表合并了 profile + socialLinks + capabilityCards，
响应时组装成前端期望的嵌套结构：
{
  name, handle, title, focus, intro, location,
  socialLinks: { githubUrl, email, bilibiliUrl, douyinUrl, xiaohongshuUrl, resumeUrl },
  capabilityCards: [{ title, tech, practice }, ...]
}
"""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class SocialLinksSchema(BaseModel):
    """与前端 socialLinks 对象对齐"""
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    github_url: str = ""
    email: str = ""
    bilibili_url: str = ""
    douyin_url: str = ""
    xiaohongshu_url: str = ""
    resume_url: str = ""


class CapabilityCardSchema(BaseModel):
    """与前端 capabilityCards 元素对齐"""
    title: str = ""
    tech: str = ""
    practice: str = ""


class ProfileResponse(BaseModel):
    """完整个人资料响应"""
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    name: str
    handle: str
    title: str
    focus: str
    intro: Optional[str] = None
    location: str
    social_links: SocialLinksSchema
    capability_cards: List[CapabilityCardSchema] = []


class ProfileUpdate(BaseModel):
    """管理端更新资料（所有字段可选）"""
    name: Optional[str] = Field(None, max_length=100)
    handle: Optional[str] = Field(None, max_length=100)
    title: Optional[str] = Field(None, max_length=300)
    focus: Optional[str] = Field(None, max_length=500)
    intro: Optional[str] = None
    location: Optional[str] = Field(None, max_length=100)

    github_url: Optional[str] = Field(None, max_length=500)
    email: Optional[str] = Field(None, max_length=300)
    bilibili_url: Optional[str] = Field(None, max_length=500)
    douyin_url: Optional[str] = Field(None, max_length=500)
    xiaohongshu_url: Optional[str] = Field(None, max_length=500)
    resume_url: Optional[str] = Field(None, max_length=500)

    capability_cards: Optional[List[CapabilityCardSchema]] = None
