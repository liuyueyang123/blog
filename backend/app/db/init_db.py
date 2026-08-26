"""数据库初始化：建表 + 创建默认管理员"""

from sqlalchemy import inspect, select

from app.db.base import engine, SessionLocal, Base
import app.models  # noqa: F401  导入全部模型，确保 Base.metadata 注册所有表
from app.models.admin import Admin
from app.core.security import hash_password


def init_db() -> None:
    """
    初始化数据库：
    1. 创建所有表（如果不存在）
    2. 创建默认管理员（如果不存在）

    生产环境应使用 Alembic migration，此脚本仅用于开发快速启动。
    """
    # 创建表
    Base.metadata.create_all(bind=engine)
    print("[OK] Database tables ready")

    # 创建默认管理员
    db = SessionLocal()
    try:
        existing = db.execute(
            select(Admin).where(Admin.username == "admin")
        ).scalar_one_or_none()

        if existing is None:
            default_admin = Admin(
                username="admin",
                password_hash=hash_password("admin123"),
                display_name="Yael",
                is_active=True,
            )
            db.add(default_admin)
            db.commit()
            print("[OK] Default admin created: admin / admin123")
            print("[WARN] Please change password after first login!")
        else:
            print("[INFO] Admin 'admin' already exists, skipping")
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
