from datetime import datetime
from uuid import UUID

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship

from app.infra.db.postgres.base import Base

class SearchHistory(Base):
    """Model for tracking user search history"""
    __tablename__ = "core_mstr_one_qlick_search_history_tbl"

    search_id = Column(PGUUID, primary_key=True, server_default="gen_random_uuid()")
    user_id = Column(PGUUID, ForeignKey("core_mstr_one_qlick_users_tbl.user_id", ondelete="CASCADE"), nullable=False)
    search_query = Column(String(255), nullable=False)
    search_type = Column(String(20), nullable=False)  # 'restaurant', 'food', 'general'
    results_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)