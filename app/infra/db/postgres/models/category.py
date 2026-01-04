from sqlalchemy import Column, String, Boolean, TIMESTAMP, Integer
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR
from sqlalchemy.sql import func
import uuid
from ..base import Base


class Category(Base):
    """Food categories model."""
    __tablename__ = 'core_mstr_one_qlick_categories_tbl'

    category_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(String)
    image = Column(String(500))
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    search_vector = Column(TSVECTOR)  # For full-text search
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
