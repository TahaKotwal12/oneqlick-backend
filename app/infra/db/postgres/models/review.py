from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Integer, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..base import Base
from app.utils.enums import ReviewType


class Review(Base):
    """Reviews and ratings model."""
    __tablename__ = 'core_mstr_one_qlick_reviews_tbl'

    review_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_orders_tbl(order_id)'))
    customer_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl(user_id)'))
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_restaurants_tbl(restaurant_id)'))
    delivery_partner_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl(user_id)'))
    rating = Column(Integer, nullable=False, CheckConstraint('rating >= 1 AND rating <= 5'))
    review_text = Column(String)
    review_type = Column(String(20), nullable=False)  # 'restaurant', 'delivery'
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
