from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey, DECIMAL, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB, TSVECTOR
from sqlalchemy.sql import func
import uuid
from ..base import Base


class FoodItem(Base):
    """Food items model."""
    __tablename__ = 'core_mstr_one_qlick_food_items_tbl'

    food_item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_restaurants_tbl.restaurant_id', ondelete='CASCADE'))
    category_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_categories_tbl.category_id'))
    name = Column(String(255), nullable=False)
    description = Column(String)
    price = Column(DECIMAL(10, 2), nullable=False)
    discount_price = Column(DECIMAL(10, 2))
    image = Column(String(500))
    is_veg = Column(Boolean, default=True)
    ingredients = Column(String)
    allergens = Column(String)
    calories = Column(Integer)
    prep_time = Column(Integer)  # in minutes
    status = Column(String(20), default='available')
    is_available = Column(Boolean, default=True, nullable=False)  # For inventory management
    rating = Column(DECIMAL(3, 2), default=0)
    total_ratings = Column(Integer, default=0)
    sort_order = Column(Integer, default=0)
    is_popular = Column(Boolean, default=False)
    is_recommended = Column(Boolean, default=False)
    nutrition_info = Column(JSONB)
    preparation_time = Column(String(20))
    search_vector = Column(TSVECTOR)  # For full-text search
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
