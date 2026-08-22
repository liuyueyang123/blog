"""故障排查管理路由（需要 JWT 认证）"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.api.deps import get_current_admin
from app.models.admin import Admin
from app.schemas.troubleshooting import (
    TroubleshootingCaseCreate,
    TroubleshootingCaseUpdate,
    TroubleshootingCaseResponse,
)
from app.services import troubleshooting as trouble_service
from app.utils.response import success, list_response

router = APIRouter(prefix="/admin/troubleshooting", tags=["故障排查管理"])


@router.get("")
def get_all_cases(
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    """获取所有案例（含未发布）"""
    cases = trouble_service.get_all_cases(db)
    total = len(cases)
    data = [TroubleshootingCaseResponse.model_validate(c).model_dump(mode="json", by_alias=True) for c in cases]
    return list_response(data=data, total=total)


@router.post("")
def create_case(
    body: TroubleshootingCaseCreate,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    """新增案例"""
    existing = trouble_service.get_case_by_slug(db, body.slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Slug '{body.slug}' already exists",
        )
    case = trouble_service.create_case(db, body)
    return success(
        data=TroubleshootingCaseResponse.model_validate(case).model_dump(mode="json", by_alias=True),
        message="Case created",
    )


@router.put("/{case_id}")
def update_case(
    case_id: int,
    body: TroubleshootingCaseUpdate,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    """更新案例"""
    case = trouble_service.get_case_by_id(db, case_id)
    if case is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")
    updated = trouble_service.update_case(db, case, body)
    return success(
        data=TroubleshootingCaseResponse.model_validate(updated).model_dump(mode="json", by_alias=True),
        message="Case updated",
    )


@router.delete("/{case_id}")
def delete_case(
    case_id: int,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    """删除案例"""
    case = trouble_service.get_case_by_id(db, case_id)
    if case is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")
    trouble_service.delete_case(db, case)
    return success(message="Case deleted")
