"""SQLAlchemy 2.0 数据库基础设施"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

from app.core.config import get_settings

settings = get_settings()

# SQLite 不支持连接池参数，需要区分处理
_db_url = settings.effective_database_url
_engine_kwargs: dict = {
    "echo": (settings.app_env == "development"),
}
if _db_url.startswith("sqlite"):
    _engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    _engine_kwargs.update(
        pool_size=10,
        max_overflow=20,
        pool_recycle=3600,      # MySQL 默认 wait_timeout=28800，1 小时回收
        pool_pre_ping=True,     # 每次取连接前 ping 一下，避免断连
    )

engine = create_engine(_db_url, **_engine_kwargs)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """所有 ORM Model 的基类（SQLAlchemy 2.0 风格）"""
    pass


def get_db():
    """FastAPI 依赖注入：提供数据库 session，请求结束自动关闭"""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
