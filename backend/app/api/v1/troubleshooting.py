"""故障排查公开路由（无需认证）"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.troubleshooting import TroubleshootingCaseResponse
from app.services import troubleshooting as trouble_service
from app.utils.response import success, list_response

router = APIRouter(prefix="/troubleshooting", tags=["故障排查（公开）"])


@router.get("")
def get_cases(db: Session = Depends(get_db)):
    """获取所有已发布故障案例"""
    cases = trouble_service.get_published_cases(db)
    total = len(cases)
    data = [TroubleshootingCaseResponse.model_validate(c).model_dump(mode="json", by_alias=True) for c in cases]
    return list_response(data=data, total=total)


@router.get("/{slug}")
def get_case(slug: str, db: Session = Depends(get_db)):
    """根据 slug 获取案例详情"""
    case = trouble_service.get_case_by_slug(db, slug)
    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Troubleshooting case not found",
        )
    return success(
        data=TroubleshootingCaseResponse.model_validate(case).model_dump(mode="json", by_alias=True)
    )
