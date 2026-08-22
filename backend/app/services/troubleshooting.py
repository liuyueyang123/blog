"""故障排查案例服务层"""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.troubleshooting import TroubleshootingCase
from app.schemas.troubleshooting import TroubleshootingCaseCreate, TroubleshootingCaseUpdate


def get_published_cases(db: Session) -> List[TroubleshootingCase]:
    """获取所有已发布案例"""
    stmt = (
        select(TroubleshootingCase)
        .where(TroubleshootingCase.is_published == True)
        .order_by(TroubleshootingCase.sort_order.asc(), TroubleshootingCase.id.asc())
    )
    return list(db.execute(stmt).scalars().all())


def get_case_by_slug(db: Session, slug: str) -> Optional[TroubleshootingCase]:
    """根据 slug 获取案例（仅限已发布）"""
    stmt = select(TroubleshootingCase).where(
        TroubleshootingCase.slug == slug,
        TroubleshootingCase.is_published == True,
    )
    return db.execute(stmt).scalar_one_or_none()


def get_all_cases(db: Session) -> List[TroubleshootingCase]:
    """获取所有案例（含未发布，管理用）"""
    stmt = select(TroubleshootingCase).order_by(
        TroubleshootingCase.sort_order.asc(), TroubleshootingCase.id.asc()
    )
    return list(db.execute(stmt).scalars().all())


def get_case_by_id(db: Session, case_id: int) -> Optional[TroubleshootingCase]:
    """根据 ID 获取案例（管理用）"""
    return db.get(TroubleshootingCase, case_id)


def create_case(db: Session, data: TroubleshootingCaseCreate) -> TroubleshootingCase:
    """创建案例"""
    case = TroubleshootingCase(**data.model_dump())
    db.add(case)
    db.commit()
    db.refresh(case)
    return case


def update_case(db: Session, case: TroubleshootingCase, data: TroubleshootingCaseUpdate) -> TroubleshootingCase:
    """更新案例"""
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(case, field, value)
    db.commit()
    db.refresh(case)
    return case


def delete_case(db: Session, case: TroubleshootingCase) -> None:
    """删除案例"""
    db.delete(case)
    db.commit()
