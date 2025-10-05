from sqlalchemy import Column, String, Boolean, TIMESTAMP, Enum, Date, Integer
from sqlalchemy.dialects.postgresql import UUID, ENUM, TIMESTAMPTZ
from sqlalchemy.sql import func
import uuid
from ..base import Base
from app.utils.enums import UserRole, UserStatus, Gender


class PendingUser(Base):
    """Pending user model for unverified registrations."""
    __tablename__ = 'core_mstr_one_qlick_pending_users_tbl'

    pending_user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)
    profile_image = Column(String(500))
    date_of_birth = Column(Date)
    gender = Column(Enum(Gender))
    verification_token = Column(String(255), unique=True, nullable=False)  # For email verification
    expires_at = Column(TIMESTAMPTZ, nullable=False)  # Token expiration
    is_verified = Column(Boolean, default=False)
    created_at = Column(TIMESTAMPTZ, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMPTZ, server_default=func.now(), onupdate=func.now(), nullable=False)
