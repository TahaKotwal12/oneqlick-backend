from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..base import Base


class RestaurantOffer(Base):
    """Restaurant offers and promotions model."""
    __tablename__ = 'core_mstr_one_qlick_restaurant_offers_tbl'

    offer_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_restaurants_tbl.restaurant_id', ondelete='CASCADE'))
    title = Column(String(255), nullable=False)
    description = Column(String)
    discount_type = Column(String(20), nullable=False)  # 'percentage', 'fixed_amount', 'free_delivery'
    discount_value = Column(DECIMAL(10, 2), nullable=False)
    min_order_amount = Column(DECIMAL(10, 2))
    max_discount_amount = Column(DECIMAL(10, 2))
    valid_from = Column(TIMESTAMP, nullable=False)
    valid_until = Column(TIMESTAMP, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

