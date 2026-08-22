"""时间线模型"""

from datetime import datetime

from sqlalchemy import String, Text, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TimelineItem(Base):
    __tablename__ = "timeline_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # 列名避免使用 MySQL 保留字 time，前端字段仍为 time
    time_label: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    detail: Mapped[str] = mapped_column(Text, nullable=False, default="")
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<TimelineItem id={self.id} title='{self.title}'>"
