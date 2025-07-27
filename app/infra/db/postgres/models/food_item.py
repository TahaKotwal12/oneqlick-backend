from sqlalchemy import Column, String, Boolean, DECIMAL, Integer, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..base import Base
import enum

class FoodStatus(str, enum.Enum):
    available = 'available'
    unavailable = 'unavailable'
    out_of_stock = 'out_of_stock'

class FoodItem(Base):
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
    prep_time = Column(Integer)
    status = Column(Enum(FoodStatus), default=FoodStatus.available)
    rating = Column(DECIMAL(3, 2), default=0)
    total_ratings = Column(Integer, default=0)
    sort_order = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False) 