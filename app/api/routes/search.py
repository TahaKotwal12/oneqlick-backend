"""
Production-grade search endpoints with PostgreSQL FTS and fuzzy matching.
Optimized for Railway deployment with NeonDB.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.infra.db.postgres.postgres_config import get_db
from app.api.dependencies import get_current_user, get_optional_current_user
from app.api.schemas.common_schemas import CommonResponse
from app.services.search_service import SearchService
from app.config.logger import get_logger
from app.utils.rate_limiter import rate_limit_search

router = APIRouter()
logger = get_logger(__name__)


@router.get("/")
@rate_limit_search()  # 50 requests/minute for search
async def global_search(
    query: str = Query(..., min_length=1, max_length=500, description="Search query"),
    latitude: float = Query(..., ge=-90, le=90, description="User's latitude"),
    longitude: float = Query(..., ge=-180, le=180, description="User's longitude"),
    radius_km: float = Query(10.0, ge=0.1, le=50, description="Search radius in kilometers"),
    limit: int = Query(20, ge=1, le=100, description="Maximum results to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    search_type: str = Query("all", regex="^(all|restaurants|dishes|categories)$", description="Type of search"),
    is_veg_only: Optional[bool] = Query(None, description="Filter for vegetarian items only"),
    is_open: Optional[bool] = Query(None, description="Filter for currently open restaurants"),
    sort_by: str = Query("relevance", regex="^(relevance|distance|rating|price_low|price_high)$", description="Sort order"),
    use_fuzzy: bool = Query(True, description="Enable fuzzy matching for typo tolerance"),
    db: Session = Depends(get_db),
    current_user = Depends(get_optional_current_user)
):
    """
    Production-grade global search with PostgreSQL FTS and fuzzy matching.
    
    Features:
    - Full-text search with weighted ranking
    - Fuzzy matching for typo tolerance (pg_trgm)
    - Location-based filtering
    - Multi-factor relevance scoring
    - Search analytics tracking
    
    Returns:
    - Unified results from restaurants, dishes, and categories
    - Sorted by relevance, distance, rating, or price
    - Includes execution time and result metadata
    """
    try:
        logger.info(f"Search request: query='{query}', type={search_type}, location=({latitude},{longitude})")
        
        # Prepare filters
        filters = {
            'is_veg_only': is_veg_only,
            'is_open': is_open
        }
        
        # Initialize search service
        search_service = SearchService(db)
        
        # Perform unified search
        search_results = search_service.unified_search(
            query=query,
            latitude=latitude,
            longitude=longitude,
            radius_km=radius_km,
            search_type=search_type,
            filters=filters,
            limit=limit,
            offset=offset,
            use_fuzzy=use_fuzzy
        )
        
        # Apply additional sorting if requested
        if sort_by != "relevance":
            results = search_results['results']
            
            if sort_by == "distance":
                results.sort(key=lambda x: x.get('distance', float('inf')))
            elif sort_by == "rating":
                results.sort(key=lambda x: x.get('rating', 0), reverse=True)
            elif sort_by == "price_low":
                results.sort(key=lambda x: x.get('price', float('inf')))
            elif sort_by == "price_high":
                results.sort(key=lambda x: x.get('price', 0), reverse=True)
            
            search_results['results'] = results
        
        # Track search in history
        if current_user:
            search_service.track_search(
                user_id=str(current_user.user_id),
                query=query,
                search_type=search_type,
                results_count=search_results['total_count'],
                filters=filters,
                location_lat=latitude,
                location_lng=longitude
            )
        
        logger.info(
            f"Search completed: {search_results['total_count']} results in "
            f"{search_results['execution_time_ms']}ms"
        )
        
        return CommonResponse(
            code=200,
            message="Search completed successfully",
            message_id="SEARCH_SUCCESS",
            data={
                'results': search_results['results'],
                'total_count': search_results['total_count'],
                'has_more': search_results['has_more'],
                'execution_time_ms': search_results['execution_time_ms'],
                'search_query': query,
                'search_type': search_type,
                'sort_by': sort_by,
                'filters': filters
            }
        )
        
    except Exception as e:
        logger.error(f"Search error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@router.get("/suggestions")
async def get_search_suggestions(
    prefix: str = Query(..., min_length=1, max_length=100, description="Search prefix"),
    limit: int = Query(10, ge=1, le=20, description="Maximum suggestions to return"),
    db: Session = Depends(get_db)
):
    """
    Get real-time search suggestions based on popular searches.
    
    Returns suggestions that start with the given prefix,
    ordered by popularity (search count).
    """
    try:
        from sqlalchemy import text
        
        # Use the database function for suggestions
        result = db.execute(
            text("SELECT * FROM get_search_suggestions(:prefix, :limit)"),
            {"prefix": prefix, "limit": limit}
        )
        
        suggestions = [
            {
                "suggestion": row[0],
                "search_count": row[1],
                "type": "popular"
            }
            for row in result
        ]
        
        return CommonResponse(
            code=200,
            message="Suggestions retrieved successfully",
            message_id="SUGGESTIONS_SUCCESS",
            data={"suggestions": suggestions}
        )
        
    except Exception as e:
        logger.error(f"Suggestions error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get suggestions: {str(e)}"
        )


@router.get("/recent")
async def get_recent_searches(
    limit: int = Query(10, ge=1, le=50, description="Maximum recent searches to return"),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get recent searches for the current user.
    
    Returns the user's search history ordered by most recent first.
    """
    try:
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
            message_id="RECENT_SEARCHES_SUCCESS",
            data={"recent_searches": recent_searches}
        )
        
    except Exception as e:
        logger.error(f"Recent searches error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get recent searches: {str(e)}"
        )


@router.delete("/recent")
async def clear_recent_searches(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Clear all recent searches for the current user.
    
    Deletes the user's entire search history.
    """
    try:
        from app.infra.db.postgres.models.search import SearchHistory
        from sqlalchemy import delete
        
        # Delete all search history for the user
        query = delete(SearchHistory).where(SearchHistory.user_id == current_user.user_id)
        result = db.execute(query)
        db.commit()
        
        deleted_count = result.rowcount
        
        return CommonResponse(
            code=200,
            message=f"Cleared {deleted_count} recent searches successfully",
            message_id="CLEAR_SEARCHES_SUCCESS",
            data={"deleted_count": deleted_count}
        )
        
    except Exception as e:
        logger.error(f"Clear searches error: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear recent searches: {str(e)}"
        )


@router.get("/popular")
async def get_popular_searches(
    limit: int = Query(10, ge=1, le=50, description="Maximum popular searches to return"),
    db: Session = Depends(get_db)
):
    """
    Get most popular search queries across all users.
    
    Returns trending searches ordered by search count.
    """
    try:
        from sqlalchemy import text
        
        # Get popular searches
        result = db.execute(
            text("""
                SELECT search_query, search_count, last_searched_at
                FROM core_mstr_one_qlick_popular_searches_tbl
                ORDER BY search_count DESC, last_searched_at DESC
                LIMIT :limit
            """),
            {"limit": limit}
        )
        
        popular_searches = [
            {
                "search_query": row[0],
                "search_count": row[1],
                "last_searched_at": row[2].isoformat() if row[2] else None
            }
            for row in result
        ]
        
        return CommonResponse(
            code=200,
            message="Popular searches retrieved successfully",
            message_id="POPULAR_SEARCHES_SUCCESS",
            data={"popular_searches": popular_searches}
        )
        
    except Exception as e:
        logger.error(f"Popular searches error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get popular searches: {str(e)}"
        )
