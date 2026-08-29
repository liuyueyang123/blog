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


def _matches_magic(ext: str, data: bytes) -> bool:
    """校验文件真实内容（magic bytes）与扩展名是否一致，防止改扩展名绕过白名单。"""
    if ext in {".jpg", ".jpeg"}:
        return data[:3] == b"\xff\xd8\xff"
    if ext == ".png":
        return data[:8] == b"\x89PNG\r\n\x1a\n"
    if ext == ".gif":
        return data[:6] in (b"GIF87a", b"GIF89a")
    if ext == ".webp":
        return len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP"
    return False


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

    settings = get_settings()
    max_size = settings.max_upload_size_mb * 1024 * 1024

    # 只读 max_size+1 字节：既限制内存占用，又能判断是否超限（避免大文件先吃满内存）
    data = await file.read(max_size + 1)
    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="空文件")
    if len(data) > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"图片超过 {settings.max_upload_size_mb}MB 限制",
        )
    if not _matches_magic(ext, data):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文件内容与扩展名不符，疑似伪造图片",
        )

    filename = f"{uuid.uuid4().hex}{ext}"
    (_ensure_upload_dir() / filename).write_bytes(data)

    return success(data={"url": f"/uploads/{filename}"}, message="上传成功")
