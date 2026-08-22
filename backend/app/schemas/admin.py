"""管理员 / 认证相关的 Pydantic v2 Schemas"""

from datetime import datetime

from pydantic import BaseModel, Field


# ── 请求 ──────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50, examples=["admin"])
    password: str = Field(..., min_length=1, max_length=128)


# ── 响应 ──────────────────────────────────────────────────

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = Field(description="过期时间（秒）")


class AdminResponse(BaseModel):
    """返回给前端的管理员信息（不含密码哈希）"""
    model_config = {"from_attributes": True}

    id: int
    username: str
    display_name: str
    is_active: bool
    created_at: datetime
