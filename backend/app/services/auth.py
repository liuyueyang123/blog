"""认证服务层：处理管理员认证逻辑"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.admin import Admin
from app.core.security import verify_password


def authenticate_admin(db: Session, username: str, password: str) -> Optional[Admin]:
    """
    验证管理员账号密码。
    成功返回 Admin 对象，失败返回 None。
    """
    stmt = select(Admin).where(Admin.username == username)
    admin = db.execute(stmt).scalar_one_or_none()

    if admin is None:
        return None
    if not admin.is_active:
        return None
    if not verify_password(password, admin.password_hash):
        return None

    return admin


def get_admin_by_username(db: Session, username: str) -> Optional[Admin]:
    """根据用户名查找管理员"""
    stmt = select(Admin).where(Admin.username == username)
    return db.execute(stmt).scalar_one_or_none()
