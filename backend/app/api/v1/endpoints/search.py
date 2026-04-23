from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.dependencies import get_db, get_current_user
from app.services.search_service import search_profiles_semantic
from app.services.hybrid_search_service import hybrid_search

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/semantic")
def semantic_search_api(
    q: str = Query(..., description="Natural language query for mentor matching"),
    limit: int = 10,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    results = search_profiles_semantic(db, q, int(user["sub"]), limit)
    return results

@router.get("/hybrid")
def hybrid_search_api(
    q: str,
    field: Optional[str] = None,
    tags: Optional[List[str]] = Query(None),
    limit: int = 10,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    results = hybrid_search(
        db=db,
        query=q,
        user_id=int(user["sub"]),
        field=field,
        tags=tags,
        limit=limit
    )

    return results
