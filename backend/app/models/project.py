"""项目模型"""

from datetime import datetime

from sqlalchemy import String, Text, Boolean, Integer, DateTime, JSON, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(200), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    subtitle: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    cover_tone: Mapped[str] = mapped_column(String(50), nullable=False, default="default")
    tags: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    role: Mapped[str] = mapped_column(Text, nullable=False, default="")
    result: Mapped[str] = mapped_column(Text, nullable=False, default="")
    overview: Mapped[str] = mapped_column(Text, nullable=False, default="")
    highlights: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    github_url: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    is_published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<Project id={self.id} slug='{self.slug}'>"
