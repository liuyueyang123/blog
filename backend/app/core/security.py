"""安全工具：JWT 生成/验证 + bcrypt 密码哈希"""

from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from jose import jwt, JWTError

from app.core.config import get_settings

settings = get_settings()

# ── 密码哈希（直接使用 bcrypt，不依赖 passlib）────────────


def hash_password(password: str) -> str:
    """明文密码 → bcrypt 哈希"""
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证明文密码与哈希是否匹配"""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


# ── JWT ───────────────────────────────────────────────────

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    生成 JWT access token。
    data 中应包含 {"sub": "username"} 作为主体标识。
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.jwt_expire_minutes)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> Optional[dict]:
    """
    解码并验证 JWT。
    成功返回 payload dict，失败（过期/篡改/格式错误）返回 None。
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return payload
    except JWTError:
        return None
