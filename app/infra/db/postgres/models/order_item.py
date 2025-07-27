from sqlalchemy import Column, String, Integer, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..base import Base

class OrderItem(Base):
    __tablename__ = 'core_mstr_one_qlick_order_items_tbl'

    order_item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_orders_tbl.order_id', ondelete='CASCADE'))
    food_item_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_food_items_tbl.food_item_id'))
    variant_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_food_variants_tbl.food_variant_id'))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    special_instructions = Column(String)
    created_at = Column(TIMESTAMP, nullable=False) 