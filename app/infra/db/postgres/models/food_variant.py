from sqlalchemy import Column, String, Boolean, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..base import Base

class FoodVariant(Base):
    __tablename__ = 'core_mstr_one_qlick_food_variants_tbl'

    food_variant_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    food_item_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_food_items_tbl.food_item_id', ondelete='CASCADE'))
    name = Column(String(100), nullable=False)
    price_adjustment = Column(DECIMAL(10, 2), default=0)
    is_default = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, nullable=False) 