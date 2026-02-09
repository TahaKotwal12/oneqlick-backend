from typing import List, Optional
from datetime import datetime
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.search import SearchHistory
from app.core.exceptions import DatabaseError

async def save_search_history(
    session: AsyncSession,
    user_id: UUID,
    search_query: str,
    search_type: str,
    results_count: int
) -> None:
    """Save a search query to history"""
    try:
        search_history = SearchHistory(
            user_id=user_id,
            search_query=search_query,
            search_type=search_type,
            results_count=results_count
        )
        session.add(search_history)
        await session.commit()
    except Exception as e:
        raise DatabaseError(f"Failed to save search history: {str(e)}")

async def get_recent_searches(
    session: AsyncSession,
    user_id: UUID,
    limit: int = 10
) -> List[SearchHistory]:
    """Get recent searches for a user"""
    try:
        query = select(SearchHistory)\
            .where(SearchHistory.user_id == user_id)\
            .order_by(SearchHistory.created_at.desc())\
            .limit(limit)
        result = await session.execute(query)
        return list(result.scalars().all())
    except Exception as e:
        raise DatabaseError(f"Failed to get recent searches: {str(e)}")

async def clear_search_history(
    session: AsyncSession,
    user_id: UUID
) -> None:
    """Clear search history for a user"""
    try:
        query = delete(SearchHistory).where(SearchHistory.user_id == user_id)
        await session.execute(query)
        await session.commit()
    except Exception as e:
        raise DatabaseError(f"Failed to clear search history: {str(e)}")