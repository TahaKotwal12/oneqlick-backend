from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey, DECIMAL, Integer, Time
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR
from sqlalchemy.sql import func
import uuid
from ..base import Base


class Restaurant(Base):
    """Restaurant model."""
    __tablename__ = 'core_mstr_one_qlick_restaurants_tbl'

    restaurant_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl.user_id'))
    name = Column(String(255), nullable=False)
    description = Column(String)
    phone = Column(String(20), nullable=False)
    email = Column(String(255))
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255))
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    latitude = Column(DECIMAL(10, 8), nullable=False)
    longitude = Column(DECIMAL(11, 8), nullable=False)
    image = Column(String(500))
    cover_image = Column(String(500))
    cuisine_type = Column(String(100))
    avg_delivery_time = Column(Integer)  # in minutes
    min_order_amount = Column(DECIMAL(10, 2), default=0)
    delivery_fee = Column(DECIMAL(10, 2), default=0)
    rating = Column(DECIMAL(3, 2), default=0)
    total_ratings = Column(Integer, default=0)
    status = Column(String(20), default='active')  # restaurant_status enum in DB
    is_open = Column(Boolean, default=True)
    opening_time = Column(Time)
    closing_time = Column(Time)
    is_veg = Column(Boolean, default=False)
    is_pure_veg = Column(Boolean, default=False)
    cost_for_two = Column(DECIMAL(10, 2))
    platform_fee = Column(DECIMAL(10, 2), default=5)
    search_vector = Column(TSVECTOR)  # For full-text search
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
