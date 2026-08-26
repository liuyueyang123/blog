"""应用配置 — 基于 pydantic-settings，从 .env 读取"""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ── 数据库 ──────────────────────────────────────────────
    # 如果设置了 database_url，直接使用（如 sqlite:///./dev.db）
    # 否则从下面的分量拼接 MySQL 连接串
    database_url: str = ""

    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = ""
    db_name: str = "portfolio_blog"

    @property
    def effective_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
            f"?charset=utf8mb4"
        )

    # ── JWT ─────────────────────────────────────────────────
    jwt_secret_key: str = "change-this-to-a-random-secret-key-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440  # 24 小时

    # ── 文件上传 ────────────────────────────────────────────
    upload_dir: str = "uploads"          # 图片存放目录（相对 cwd 或绝对路径）
    max_upload_size_mb: int = 5          # 单张图片大小上限（MB）

    # ── 应用 ────────────────────────────────────────────────
    app_env: str = "development"
    cors_origins: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]


@lru_cache
def get_settings() -> Settings:
    """缓存配置实例，整个应用生命周期只创建一次"""
    return Settings()
