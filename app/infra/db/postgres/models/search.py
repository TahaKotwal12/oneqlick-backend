"""
Search-related database models.
"""

from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey, DECIMAL, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from ..base import Base



class SearchHistory(Base):
    """
    Search history model for tracking user searches.
    Used for analytics and recent searches feature.
    """
    __tablename__ = 'core_mstr_one_qlick_search_history_tbl'
    
    search_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl.user_id', ondelete='CASCADE'))
    search_query = Column(String(500), nullable=False)
    search_type = Column(String(50))
    results_count = Column(Integer, default=0)
    filters = Column(JSONB)
    location_lat = Column(DECIMAL(10, 8))
    location_lng = Column(DECIMAL(11, 8))
    clicked_result_id = Column(UUID(as_uuid=True))
    clicked_result_type = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)


class PopularSearch(Base):
    """
    Popular searches cache model.
    Stores frequently searched queries for suggestions.
    """
    __tablename__ = 'core_mstr_one_qlick_popular_searches_tbl'
    
    popular_search_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    search_query = Column(String(500), nullable=False, unique=True)
    search_count = Column(Integer, default=1)
    last_searched_at = Column(TIMESTAMP, server_default=func.now())
    cached_results = Column(JSONB)
    cache_expires_at = Column(TIMESTAMP)
    location_based = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
