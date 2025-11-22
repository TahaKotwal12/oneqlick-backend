from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.auth import get_current_user_id
from app.api.schemas.search_schemas import RecentSearchResponse, RecentSearchesResponse
from app.repositories import search_repository
from app.core.responses import CommonResponse

router = APIRouter()

@router.get("/recent", response_model=CommonResponse[RecentSearchesResponse])
async def get_recent_searches(
    limit: int = 10,
    current_user_id = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """Get recent searches for the current user"""
    searches = await search_repository.get_recent_searches(session, current_user_id, limit)
    
    recent_searches = [
        RecentSearchResponse(
            search_query=search.search_query,
            search_type=search.search_type,
            results_count=search.results_count,
            created_at=search.created_at.isoformat()
        ) for search in searches
    ]
    
    return CommonResponse(
        success=True,
        message="Recent searches retrieved successfully",
        data=RecentSearchesResponse(recent_searches=recent_searches)
    )

@router.delete("/recent", response_model=CommonResponse)
async def clear_recent_searches(
    current_user_id = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """Clear all recent searches for the current user"""
    await search_repository.clear_search_history(session, current_user_id)
    
    return CommonResponse(
        success=True,
        message="Recent searches cleared successfully"
    )