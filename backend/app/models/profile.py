"""个人资料模型（单行配置表，合并 profile + socialLinks + capabilityCards）"""

from datetime import datetime

from sqlalchemy import String, Text, DateTime, JSON, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Profile(Base):
    __tablename__ = "profile"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # ── 基本信息 ──
    name: Mapped[str] = mapped_column(String(100), nullable=False, default="Yael")
    handle: Mapped[str] = mapped_column(String(100), nullable=False, default="yael")
    title: Mapped[str] = mapped_column(String(300), nullable=False, default="")
    focus: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    intro: Mapped[str] = mapped_column(Text, nullable=True)
    location: Mapped[str] = mapped_column(String(100), nullable=False, default="China")

    # ── 社交链接 ──
    github_url: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    email: Mapped[str] = mapped_column(String(300), nullable=False, default="")
    bilibili_url: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    douyin_url: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    xiaohongshu_url: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    resume_url: Mapped[str] = mapped_column(String(500), nullable=False, default="")

    # ── 首页能力卡片 [{title, tech, practice}, ...] ──
    capability_cards: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<Profile id={self.id} name='{self.name}'>"
