"""项目管理路由（需要 JWT 认证）"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.api.deps import get_current_admin
from app.models.admin import Admin
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.services import project as project_service
from app.utils.response import success, list_response

router = APIRouter(prefix="/admin/projects", tags=["项目管理"])


@router.get("")
def get_all_projects(
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    """获取所有项目（含未发布）"""
    projects = project_service.get_all_projects(db)
    total = len(projects)
    data = [ProjectResponse.model_validate(p).model_dump(mode="json", by_alias=True) for p in projects]
    return list_response(data=data, total=total)


@router.post("")
def create_project(
    body: ProjectCreate,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    """新增项目"""
    existing = project_service.get_project_by_slug(db, body.slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Slug '{body.slug}' already exists",
        )
    project = project_service.create_project(db, body)
    return success(
        data=ProjectResponse.model_validate(project).model_dump(mode="json", by_alias=True),
        message="Project created",
    )


@router.put("/{project_id}")
def update_project(
    project_id: int,
    body: ProjectUpdate,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    """更新项目"""
    project = project_service.get_project_by_id(db, project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    updated = project_service.update_project(db, project, body)
    return success(
        data=ProjectResponse.model_validate(updated).model_dump(mode="json", by_alias=True),
        message="Project updated",
    )


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    """删除项目"""
    project = project_service.get_project_by_id(db, project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    project_service.delete_project(db, project)
    return success(message="Project deleted")
