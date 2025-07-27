from sqlalchemy import Column, String, Boolean, DECIMAL, Integer, TIMESTAMP, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..base import Base
import enum

class CouponType(str, enum.Enum):
    percentage = 'percentage'
    fixed_amount = 'fixed_amount'
    free_delivery = 'free_delivery'

class Coupon(Base):
    __tablename__ = 'core_mstr_one_qlick_coupons_tbl'

    coupon_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String)
    coupon_type = Column(Enum(CouponType), nullable=False)
    discount_value = Column(DECIMAL(10, 2), nullable=False)
    min_order_amount = Column(DECIMAL(10, 2), default=0)
    max_discount_amount = Column(DECIMAL(10, 2))
    usage_limit = Column(Integer)
    used_count = Column(Integer, default=0)
    valid_from = Column(TIMESTAMP, nullable=False)
    valid_until = Column(TIMESTAMP, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, nullable=False) 