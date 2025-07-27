from sqlalchemy import Column, String, Boolean, Enum, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..base import Base
import enum

class UserRole(str, enum.Enum):
    customer = 'customer'
    admin = 'admin'
    delivery_partner = 'delivery_partner'
    restaurant_owner = 'restaurant_owner'

class UserStatus(str, enum.Enum):
    active = 'active'
    inactive = 'inactive'
    suspended = 'suspended'

class User(Base):
    __tablename__ = 'core_mstr_one_qlick_users_tbl'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.active)
    profile_image = Column(String(500))
    email_verified = Column(Boolean, default=False)
    phone_verified = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False) 