from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, DECIMAL, Enum, Integer, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..base import Base
from app.utils.enums import OrderStatus, PaymentStatus, PaymentMethod


class Order(Base):
    """Orders model."""
    __tablename__ = 'core_mstr_one_qlick_orders_tbl'
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_order_rating_range'),
    )

    order_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl.user_id'))
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_restaurants_tbl.restaurant_id'))
    delivery_partner_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl.user_id'))
    delivery_address_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_addresses_tbl.address_id'))
    order_number = Column(String(50), unique=True, nullable=False)
    subtotal = Column(DECIMAL(10, 2), nullable=False)
    tax_amount = Column(DECIMAL(10, 2), default=0)
    delivery_fee = Column(DECIMAL(10, 2), default=0)
    discount_amount = Column(DECIMAL(10, 2), default=0)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    payment_method = Column(Enum(PaymentMethod, values_callable=lambda x: [e.value for e in x]))
    payment_status = Column(Enum(PaymentStatus, values_callable=lambda x: [e.value for e in x]), default=PaymentStatus.PENDING)
    payment_id = Column(String(255))  # Payment gateway transaction ID
    order_status = Column(Enum(OrderStatus, values_callable=lambda x: [e.value for e in x]), default=OrderStatus.PENDING)
    estimated_delivery_time = Column(TIMESTAMP)
    actual_delivery_time = Column(TIMESTAMP)
    special_instructions = Column(String)
    cancellation_reason = Column(String)
    rating = Column(Integer)
    review = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
