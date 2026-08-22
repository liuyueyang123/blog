"""FastAPI 依赖注入"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.core.security import decode_access_token
from app.services.auth import get_admin_by_username
from app.models.admin import Admin

# 使用 HTTPBearer 方案（Authorization: Bearer <token>）
bearer_scheme = HTTPBearer()


def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Admin:
    """
    从 JWT 中解析当前管理员。
    用于所有 /api/v1/admin/* 路由的依赖。
    """
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效或已过期的 token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的 token 载荷",
        )

    admin = get_admin_by_username(db, username)
    if admin is None or not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="管理员不存在或已被禁用",
        )

    return admin
