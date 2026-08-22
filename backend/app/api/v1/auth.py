"""认证路由：登录 / 获取当前管理员信息"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.core.config import get_settings
from app.core.security import create_access_token
from app.schemas.admin import LoginRequest, TokenResponse, AdminResponse
from app.services.auth import authenticate_admin
from app.api.deps import get_current_admin
from app.models.admin import Admin
from app.utils.response import success, error

settings = get_settings()

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/login")
def login(body: LoginRequest, db: Session = Depends(get_db)):
    """
    管理员登录。
    成功返回 JWT token，失败返回 401。
    """
    admin = authenticate_admin(db, body.username, body.password)
    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )

    access_token = create_access_token(data={"sub": admin.username})
    expires_in = settings.jwt_expire_minutes * 60

    return success(
        data=TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=expires_in,
        ).model_dump()
    )


@router.get("/me")
def get_me(current_admin: Admin = Depends(get_current_admin)):
    """
    获取当前登录管理员信息（需要 JWT）。
    """
    return success(
        data=AdminResponse.model_validate(current_admin).model_dump(mode="json")
    )
