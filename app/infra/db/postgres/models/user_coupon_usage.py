from sqlalchemy import Column, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..base import Base


class UserCouponUsage(Base):
    """User coupon usage tracking model."""
    __tablename__ = 'core_mstr_one_qlick_user_coupon_usage_tbl'

    user_coupon_usage_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl(user_id)'))
    coupon_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_coupons_tbl(coupon_id)'))
    order_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_orders_tbl(order_id)'))
    used_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'coupon_id', 'order_id', name='unique_user_coupon_order'),
    )
