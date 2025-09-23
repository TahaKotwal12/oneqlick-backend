from sqlalchemy import Column, String, Boolean, TIMESTAMP, Enum, Date, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..base import Base
from app.utils.enums import UserRole, UserStatus, Gender


class User(Base):
    """User model for customers, admins, delivery partners, and restaurant owners."""
    __tablename__ = 'core_mstr_one_qlick_users_tbl'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)
    profile_image = Column(String(500))
    email_verified = Column(Boolean, default=False)
    phone_verified = Column(Boolean, default=False)
    date_of_birth = Column(Date)
    gender = Column(Enum(Gender))
    loyalty_points = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
