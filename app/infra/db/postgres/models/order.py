from sqlalchemy import Column, String, Boolean, DECIMAL, Integer, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..base import Base
import enum

class OrderStatus(str, enum.Enum):
    pending = 'pending'
    confirmed = 'confirmed'
    preparing = 'preparing'
    ready_for_pickup = 'ready_for_pickup'
    picked_up = 'picked_up'
    delivered = 'delivered'
    cancelled = 'cancelled'
    refunded = 'refunded'

class PaymentStatus(str, enum.Enum):
    pending = 'pending'
    paid = 'paid'
    failed = 'failed'
    refunded = 'refunded'

class PaymentMethod(str, enum.Enum):
    cash = 'cash'
    card = 'card'
    upi = 'upi'
    wallet = 'wallet'

class Order(Base):
    __tablename__ = 'core_mstr_one_qlick_orders_tbl'

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
    payment_method = Column(Enum(PaymentMethod))
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.pending)
    payment_id = Column(String(255))
    order_status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    estimated_delivery_time = Column(TIMESTAMP)
    actual_delivery_time = Column(TIMESTAMP)
    special_instructions = Column(String)
    cancellation_reason = Column(String)
    rating = Column(Integer)
    review = Column(String)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False) 