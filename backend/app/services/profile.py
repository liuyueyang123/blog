"""个人资料服务层"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.profile import Profile
from app.schemas.profile import ProfileUpdate, ProfileResponse, SocialLinksSchema, CapabilityCardSchema


def get_profile(db: Session) -> Optional[Profile]:
    """获取个人资料（单行表，取第一条）"""
    stmt = select(Profile).limit(1)
    return db.execute(stmt).scalar_one_or_none()


def get_or_create_profile(db: Session) -> Profile:
    """获取资料，不存在则创建空资料"""
    profile = get_profile(db)
    if profile is None:
        profile = Profile()
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile


def update_profile(db: Session, profile: Profile, data: ProfileUpdate) -> Profile:
    """更新资料（capability_cards 为 dict 列表，直接存 JSON）"""
    update_data = data.model_dump(exclude_unset=True)
    if "capability_cards" in update_data and update_data["capability_cards"] is not None:
        update_data["capability_cards"] = [
            c if isinstance(c, dict) else c
            for c in update_data["capability_cards"]
        ]
    for field, value in update_data.items():
        setattr(profile, field, value)
    db.commit()
    db.refresh(profile)
    return profile


def profile_to_response(profile: Profile) -> ProfileResponse:
    """将扁平的 Profile 行组装为嵌套响应结构"""
    return ProfileResponse(
        name=profile.name,
        handle=profile.handle,
        title=profile.title,
        focus=profile.focus,
        intro=profile.intro,
        location=profile.location,
        social_links=SocialLinksSchema(
            github_url=profile.github_url,
            email=profile.email,
            bilibili_url=profile.bilibili_url,
            douyin_url=profile.douyin_url,
            xiaohongshu_url=profile.xiaohongshu_url,
            resume_url=profile.resume_url,
        ),
        capability_cards=[
            CapabilityCardSchema(**card) for card in (profile.capability_cards or [])
        ],
    )
