from sqlalchemy import Column, String, Boolean, TIMESTAMP, DECIMAL, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..base import Base
from app.utils.enums import CouponType


class Coupon(Base):
    """Coupons and discounts model."""
    __tablename__ = 'core_mstr_one_qlick_coupons_tbl'

    coupon_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String)
    coupon_type = Column(Enum(CouponType, native_enum=True, name='coupontype', create_constraint=True, validate_strings=True), nullable=False)
    discount_value = Column(DECIMAL(10, 2), nullable=False)
    min_order_amount = Column(DECIMAL(10, 2), default=0)
    max_discount_amount = Column(DECIMAL(10, 2))
    usage_limit = Column(Integer)
    used_count = Column(Integer, default=0)
    valid_from = Column(TIMESTAMP, nullable=False)
    valid_until = Column(TIMESTAMP, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    
    # Carousel display fields
    show_in_carousel = Column(Boolean, default=False)
    carousel_priority = Column(Integer, default=0)
    carousel_title = Column(String(100))
    carousel_subtitle = Column(String(100))
    carousel_badge = Column(String(50))
    carousel_icon = Column(String(50))
    carousel_gradient_start = Column(String(7), default='#4F46E5')
    carousel_gradient_middle = Column(String(7), default='#6366F1')
    carousel_gradient_end = Column(String(7), default='#818CF8')
    carousel_action_text = Column(String(50), default='Order Now')
