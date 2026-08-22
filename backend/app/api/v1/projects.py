"""项目公开路由（无需认证）"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.project import ProjectResponse
from app.services import project as project_service
from app.utils.response import success, list_response

router = APIRouter(prefix="/projects", tags=["项目（公开）"])


@router.get("")
def get_projects(db: Session = Depends(get_db)):
    """获取所有已发布项目列表"""
    projects = project_service.get_published_projects(db)
    total = len(projects)
    data = [ProjectResponse.model_validate(p).model_dump(mode="json", by_alias=True) for p in projects]
    return list_response(data=data, total=total)


@router.get("/{slug}")
def get_project(slug: str, db: Session = Depends(get_db)):
    """根据 slug 获取项目详情"""
    project = project_service.get_project_by_slug(db, slug)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    return success(
        data=ProjectResponse.model_validate(project).model_dump(mode="json", by_alias=True)
    )
