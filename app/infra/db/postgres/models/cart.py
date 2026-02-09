from sqlalchemy import Column, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..base import Base


class Cart(Base):
    """Shopping cart model."""
    __tablename__ = 'core_mstr_one_qlick_cart_tbl'

    cart_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl.user_id', ondelete='CASCADE'))
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_restaurants_tbl.restaurant_id'))
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
