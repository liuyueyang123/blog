"""统一 API 响应格式"""

from typing import Any, Optional, List

from pydantic import BaseModel


class ApiResponse(BaseModel):
    """
    统一响应体，与前端约定：
    {
        "code": 0,
        "message": "ok",
        "data": ...,
        "total": null       # 仅列表接口返回
    }
    """
    code: int = 0
    message: str = "ok"
    data: Any = None
    total: Optional[int] = None


def success(data: Any = None, message: str = "ok", total: Optional[int] = None) -> dict:
    """成功响应"""
    result = {"code": 0, "message": message, "data": data}
    if total is not None:
        result["total"] = total
    return result


def error(code: int, message: str, data: Any = None) -> dict:
    """错误响应"""
    return {"code": code, "message": message, "data": data}


def list_response(data: List[Any], total: int, message: str = "ok") -> dict:
    """列表响应"""
    return {"code": 0, "message": message, "data": data, "total": total}
