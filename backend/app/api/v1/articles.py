"""文章公开路由（无需认证）"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.article import ArticleResponse
from app.services import article as article_service
from app.utils.response import success, list_response

router = APIRouter(prefix="/articles", tags=["文章（公开）"])


@router.get("")
def get_articles(db: Session = Depends(get_db)):
    """获取所有已发布文章列表"""
    articles = article_service.get_published_articles(db)
    total = len(articles)
    data = [ArticleResponse.model_validate(a).model_dump(mode="json", by_alias=True) for a in articles]
    return list_response(data=data, total=total)


@router.get("/{slug}")
def get_article(slug: str, db: Session = Depends(get_db)):
    """根据 slug 获取文章详情"""
    article = article_service.get_article_by_slug(db, slug)
    if article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
    return success(
        data=ArticleResponse.model_validate(article).model_dump(mode="json", by_alias=True)
    )
