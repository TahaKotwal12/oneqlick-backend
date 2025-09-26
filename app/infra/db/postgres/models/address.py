from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey, DECIMAL, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..base import Base
from app.utils.enums import AddressType


class Address(Base):
    """User addresses model."""
    __tablename__ = 'core_mstr_one_qlick_addresses_tbl'

    address_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl(user_id)', ondelete='CASCADE'))
    title = Column(String(100), nullable=False)  # Home, Office, etc.
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255))
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    is_default = Column(Boolean, default=False)
    address_type = Column(Enum(AddressType), default=AddressType.HOME)
    landmark = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
  