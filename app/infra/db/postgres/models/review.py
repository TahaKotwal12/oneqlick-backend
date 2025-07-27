from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..base import Base

class Review(Base):
    __tablename__ = 'core_mstr_one_qlick_reviews_tbl'

    review_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_orders_tbl.order_id'))
    customer_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl.user_id'))
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_restaurants_tbl.restaurant_id'))
    delivery_partner_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl.user_id'))
    rating = Column(Integer, nullable=False)
    review_text = Column(String)
    review_type = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False) 