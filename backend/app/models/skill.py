"""技能模型：技能组（1）→ 技能项（N）"""

from datetime import datetime
from typing import List

from sqlalchemy import String, Text, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class SkillGroup(Base):
    __tablename__ = "skill_groups"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    summary: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    # 1:N 关系，删除组时级联删除项
    items: Mapped[List["SkillItem"]] = relationship(
        back_populates="group",
        cascade="all, delete-orphan",
        order_by="SkillItem.sort_order",
    )

    def __repr__(self) -> str:
        return f"<SkillGroup id={self.id} title='{self.title}'>"


class SkillItem(Base):
    __tablename__ = "skill_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_id: Mapped[int] = mapped_column(
        ForeignKey("skill_groups.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    direction: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    scenario: Mapped[str] = mapped_column(Text, nullable=False, default="")
    # 4 级状态，用 String 存储（Pydantic 层做枚举校验），避免 MySQL ENUM 迁移麻烦
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="正在系统学习")
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    group: Mapped["SkillGroup"] = relationship(back_populates="items")

    def __repr__(self) -> str:
        return f"<SkillItem id={self.id} name='{self.name}'>"
