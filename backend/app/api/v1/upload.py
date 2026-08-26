"""图片上传路由（需要 JWT 认证）"""

import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.api.deps import get_current_admin
from app.core.config import get_settings
from app.models.admin import Admin
from app.utils.response import success

router = APIRouter(prefix="/admin", tags=["图片上传"])

# 只允许栅格图；排除 SVG 以避免潜在注入风险
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


def _ensure_upload_dir() -> Path:
    upload_dir = Path(get_settings().upload_dir).resolve()
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir


@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    _admin: Admin = Depends(get_current_admin),
):
    """上传图片，返回可访问的相对 URL（/uploads/<filename>）"""
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支持的图片格式 {ext or '(无扩展名)'}，仅支持 {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )

    data = await file.read()
    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="空文件")

    settings = get_settings()
    max_size = settings.max_upload_size_mb * 1024 * 1024
    if len(data) > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"图片超过 {settings.max_upload_size_mb}MB 限制",
        )

    filename = f"{uuid.uuid4().hex}{ext}"
    (_ensure_upload_dir() / filename).write_bytes(data)

    return success(data={"url": f"/uploads/{filename}"}, message="上传成功")
