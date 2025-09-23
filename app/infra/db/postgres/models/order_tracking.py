from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, DECIMAL, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..base import Base
from app.utils.enums import OrderStatus


class OrderTracking(Base):
    """Order tracking model."""
    __tablename__ = 'core_mstr_one_qlick_order_tracking_tbl'

    order_tracking_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_orders_tbl(order_id)', ondelete='CASCADE'))
    status = Column(Enum(OrderStatus), nullable=False)
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    notes = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
