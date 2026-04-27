from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.dependencies import get_db, get_current_user
from app.models.article import Article
from app.models.user import User
import slugify

router = APIRouter(prefix="/kb", tags=["Knowledge Base"])

@router.post("/articles")
def create_article(
    data: dict, 
    db: Session = Depends(get_db), 
    user = Depends(get_current_user)
):
    """
    Create a new article in the knowledge base. Mentors only in production.
    """
    article = Article(
        author_id=str(user["sub"]),
        title=data["title"],
        slug=slugify.slugify(data["title"]),
        content=data["content"],
        category=data.get("category", "General")
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return article

@router.get("/articles")
def list_articles(
    category: Optional[str] = None,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    query = db.query(Article)
    if category:
        query = query.filter(Article.category == category)
    return query.order_by(Article.created_at.desc()).limit(limit).all()

@router.get("/articles/{slug}")
def get_article(slug: str, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.slug == slug).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Track view
    article.views += 1
    db.commit()
    
    return article
