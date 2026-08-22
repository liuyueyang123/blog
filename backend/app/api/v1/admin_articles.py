"""文章管理路由（需要 JWT 认证）"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.api.deps import get_current_admin
from app.models.admin import Admin
from app.schemas.article import ArticleCreate, ArticleUpdate, ArticleResponse
from app.services import article as article_service
from app.utils.response import success, list_response

router = APIRouter(prefix="/admin/articles", tags=["文章管理"])


@router.get("")
def get_all_articles(
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    """获取所有文章（含未发布）"""
    articles = article_service.get_all_articles(db)
    total = len(articles)
    data = [ArticleResponse.model_validate(a).model_dump(mode="json", by_alias=True) for a in articles]
    return list_response(data=data, total=total)


@router.post("")
def create_article(
    body: ArticleCreate,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    """新增文章"""
    # 检查 slug 是否已存在
    existing = article_service.get_article_by_slug(db, body.slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Slug '{body.slug}' already exists",
        )
    article = article_service.create_article(db, body)
    return success(
        data=ArticleResponse.model_validate(article).model_dump(mode="json", by_alias=True),
        message="Article created",
    )


@router.put("/{article_id}")
def update_article(
    article_id: int,
    body: ArticleUpdate,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    """更新文章"""
    article = article_service.get_article_by_id(db, article_id)
    if article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
    updated = article_service.update_article(db, article, body)
    return success(
        data=ArticleResponse.model_validate(updated).model_dump(mode="json", by_alias=True),
        message="Article updated",
    )


@router.delete("/{article_id}")
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    """删除文章"""
    article = article_service.get_article_by_id(db, article_id)
    if article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
    article_service.delete_article(db, article)
    return success(message="Article deleted")
