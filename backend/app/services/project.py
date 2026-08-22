"""项目服务层：CRUD 业务逻辑"""

from typing import List, Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


def get_published_projects(db: Session) -> List[Project]:
    """获取所有已发布项目（按 sort_order 升序）"""
    stmt = (
        select(Project)
        .where(Project.is_published == True)
        .order_by(Project.sort_order.asc(), Project.id.asc())
    )
    return list(db.execute(stmt).scalars().all())


def get_project_by_slug(db: Session, slug: str) -> Optional[Project]:
    """根据 slug 获取项目（仅限已发布）"""
    stmt = select(Project).where(
        Project.slug == slug,
        Project.is_published == True,
    )
    return db.execute(stmt).scalar_one_or_none()


def get_all_projects(db: Session) -> List[Project]:
    """获取所有项目（含未发布，管理用）"""
    stmt = select(Project).order_by(Project.sort_order.asc(), Project.id.asc())
    return list(db.execute(stmt).scalars().all())


def get_project_by_id(db: Session, project_id: int) -> Optional[Project]:
    """根据 ID 获取项目（管理用）"""
    return db.get(Project, project_id)


def create_project(db: Session, data: ProjectCreate) -> Project:
    """创建项目"""
    project = Project(**data.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def update_project(db: Session, project: Project, data: ProjectUpdate) -> Project:
    """更新项目（只更新传入的字段）"""
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project: Project) -> None:
    """删除项目"""
    db.delete(project)
    db.commit()


def count_projects(db: Session, published_only: bool = False) -> int:
    """统计项目数量"""
    stmt = select(func.count(Project.id))
    if published_only:
        stmt = stmt.where(Project.is_published == True)
    return db.execute(stmt).scalar() or 0
