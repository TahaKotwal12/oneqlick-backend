from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.infra.db.postgres.postgres_config import get_db
from app.api.dependencies import get_current_user
from app.api.schemas.search_schemas import RecentSearchResponse, RecentSearchesResponse
from app.api.schemas.common_schemas import CommonResponse

router = APIRouter()

@router.get("/recent")
def get_recent_searches(
    limit: int = 10,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get recent searches for the current user"""
    from app.infra.db.postgres.models.search import SearchHistory
    from sqlalchemy import select
    
    # Get recent searches
    query = select(SearchHistory)\
        .where(SearchHistory.user_id == current_user.user_id)\
        .order_by(SearchHistory.created_at.desc())\
        .limit(limit)
    
    searches = db.execute(query).scalars().all()
    
    recent_searches = [
        {
            "search_query": search.search_query,
            "search_type": search.search_type,
            "results_count": search.results_count,
            "created_at": search.created_at.isoformat()
        } for search in searches
    ]
    
    return CommonResponse(
        code=200,
        message="Recent searches retrieved successfully",
        message_id="0",
        data={"recent_searches": recent_searches}
    )

@router.delete("/recent")
def clear_recent_searches(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Clear all recent searches for the current user"""
    from app.infra.db.postgres.models.search import SearchHistory
    from sqlalchemy import delete
    
    # Delete all search history for the user
    query = delete(SearchHistory).where(SearchHistory.user_id == current_user.user_id)
    db.execute(query)
    db.commit()
    
    return CommonResponse(
        code=200,
        message="Recent searches cleared successfully",
        message_id="0",
        data={}
    )