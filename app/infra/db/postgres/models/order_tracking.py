from sqlalchemy import Column, String, DECIMAL, TIMESTAMP, ForeignKey, Enum
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

class OrderTracking(Base):
    __tablename__ = 'core_mstr_one_qlick_order_tracking_tbl'

    order_tracking_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_orders_tbl.order_id', ondelete='CASCADE'))
    status = Column(Enum(OrderStatus), nullable=False)
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    notes = Column(String)
    created_at = Column(TIMESTAMP, nullable=False) 