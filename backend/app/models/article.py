"""文章模型"""

from datetime import date, datetime

from sqlalchemy import String, Text, Date, Boolean, Integer, DateTime, JSON, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(200), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    excerpt: Mapped[str] = mapped_column(Text, nullable=False, default="")
    date: Mapped[date] = mapped_column(Date, nullable=False)
    read_time: Mapped[str] = mapped_column(String(50), nullable=False, default="5 min")
    content: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    is_published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<Article id={self.id} slug='{self.slug}'>"
