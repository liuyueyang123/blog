"""一次性迁移：articles.content 从 JSON 字符串数组改为 Markdown 字符串（LONGTEXT）"""

import json

from sqlalchemy import select, text

from app.db.base import SessionLocal, engine
from app.models.article import Article


def normalize(content) -> str:
    """把旧的 JSON 数组文本归一化成 markdown 字符串，已是 markdown 字符串则原样返回。"""
    if isinstance(content, list):
        return "\n\n".join(str(item) for item in content)
    if isinstance(content, str):
        stripped = content.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            try:
                parsed = json.loads(stripped)
                if isinstance(parsed, list):
                    return "\n\n".join(str(item) for item in parsed)
            except (ValueError, TypeError):
                pass
        return content
    return ""


def migrate() -> None:
    # 1) 先把列从 JSON 改成 LONGTEXT（MySQL 会把 JSON 值自动转成文本表示）
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE articles MODIFY content LONGTEXT NOT NULL"))
    print("[OK] ALTER TABLE articles MODIFY content LONGTEXT NOT NULL")

    # 2) 再把旧的 JSON 数组文本归一化成 markdown 字符串
    db = SessionLocal()
    try:
        rows = list(db.execute(select(Article)).scalars())
        converted = 0
        for article in rows:
            new_content = normalize(article.content)
            if new_content != article.content:
                article.content = new_content
                converted += 1
        db.commit()
        print(f"[OK] content normalized: {converted}/{len(rows)} rows converted")
    finally:
        db.close()


if __name__ == "__main__":
    migrate()
