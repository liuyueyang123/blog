"""文章服务层：CRUD 业务逻辑"""

from typing import List, Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.article import Article
from app.schemas.article import ArticleCreate, ArticleUpdate


def get_published_articles(db: Session) -> List[Article]:
    """获取所有已发布文章（按日期倒序）"""
    stmt = (
        select(Article)
        .where(Article.is_published == True)
        .order_by(Article.date.desc(), Article.sort_order.asc())
    )
    return list(db.execute(stmt).scalars().all())


def get_article_by_slug(db: Session, slug: str) -> Optional[Article]:
    """根据 slug 获取文章（仅限已发布）"""
    stmt = select(Article).where(
        Article.slug == slug,
        Article.is_published == True,
    )
    return db.execute(stmt).scalar_one_or_none()


def get_all_articles(db: Session) -> List[Article]:
    """获取所有文章（含未发布，管理用）"""
    stmt = select(Article).order_by(Article.date.desc(), Article.sort_order.asc())
    return list(db.execute(stmt).scalars().all())


def get_article_by_id(db: Session, article_id: int) -> Optional[Article]:
    """根据 ID 获取文章（管理用）"""
    return db.get(Article, article_id)


def create_article(db: Session, data: ArticleCreate) -> Article:
    """创建文章"""
    article = Article(**data.model_dump())
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


def update_article(db: Session, article: Article, data: ArticleUpdate) -> Article:
    """更新文章（只更新传入的字段）"""
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(article, field, value)
    db.commit()
    db.refresh(article)
    return article


def delete_article(db: Session, article: Article) -> None:
    """删除文章"""
    db.delete(article)
    db.commit()


def count_articles(db: Session, published_only: bool = False) -> int:
    """统计文章数量"""
    stmt = select(func.count(Article.id))
    if published_only:
        stmt = stmt.where(Article.is_published == True)
    return db.execute(stmt).scalar() or 0
