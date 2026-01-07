from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..base import Base


class CartItem(Base):
    """Cart items model."""
    __tablename__ = 'core_mstr_one_qlick_cart_items_tbl'

    cart_item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cart_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_cart_tbl.cart_id', ondelete='CASCADE'))
    food_item_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_food_items_tbl.food_item_id'))
    variant_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_food_variants_tbl.food_variant_id'), nullable=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False, default=0.00)
    total_price = Column(Numeric(10, 2), nullable=False, default=0.00)
    special_instructions = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
