"""修改后台管理员用户名 / 密码（密码走环境变量，不落库明文、不进仓库）

用法（在 backend 目录下，用 venv python）：
    ADMIN_NEW_USERNAME=lyy ADMIN_NEW_PASSWORD='你的新密码' ./venv/bin/python -m app.db.update_admin

可选：
    ADMIN_OLD_USERNAME  默认 "admin"，用于定位要改的那条管理员记录；找不到时兜底取第一条管理员。
"""

import os

from sqlalchemy import select

from app.db.base import SessionLocal
from app.models.admin import Admin
from app.core.security import hash_password

DEFAULT_OLD_USERNAME = "admin"


def update_admin(old_username: str, new_username: str, new_password: str) -> None:
    """定位并更新管理员：改用户名 + 重置密码。"""
    if not new_username or not new_password:
        raise SystemExit("[ERROR] 新用户名 / 新密码不能为空，请通过环境变量传入")

    if len(new_password) < 8:
        print("[WARN] 密码长度小于 8 位，建议使用更长的密码")

    db = SessionLocal()
    try:
        admin = db.execute(
            select(Admin).where(Admin.username == old_username)
        ).scalar_one_or_none()

        # 兜底：old_username 匹配不到时，取第一条管理员记录
        if admin is None:
            admin = db.execute(select(Admin).order_by(Admin.id)).scalars().first()

        if admin is None:
            raise SystemExit("[ERROR] 未找到任何管理员，请先运行 init_db")

        conflict = db.execute(
            select(Admin).where(Admin.username == new_username, Admin.id != admin.id)
        ).scalar_one_or_none()
        if conflict is not None:
            raise SystemExit(f"[ERROR] 用户名 {new_username!r} 已被占用")

        old = admin.username
        admin.username = new_username
        admin.password_hash = hash_password(new_password)
        db.commit()
        print(f"[OK] 管理员已更新：{old} -> {new_username}")
        print("[OK] 密码已更新（bcrypt 加密存储）")
    finally:
        db.close()


if __name__ == "__main__":
    update_admin(
        old_username=os.environ.get("ADMIN_OLD_USERNAME", DEFAULT_OLD_USERNAME),
        new_username=os.environ.get("ADMIN_NEW_USERNAME", ""),
        new_password=os.environ.get("ADMIN_NEW_PASSWORD", ""),
    )
