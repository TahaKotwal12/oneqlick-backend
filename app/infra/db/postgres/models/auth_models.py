from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey, Enum, func, Text, Integer, INET
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from ..base import Base
import enum

class AuthProvider(str, enum.Enum):
    google = 'google'
    facebook = 'facebook'
    apple = 'apple'

class OTPType(str, enum.Enum):
    phone_verification = 'phone_verification'
    email_verification = 'email_verification'
    password_reset = 'password_reset'

class DeviceType(str, enum.Enum):
    mobile = 'mobile'
    web = 'web'
    tablet = 'tablet'

class Platform(str, enum.Enum):
    ios = 'ios'
    android = 'android'
    web = 'web'

class RefreshToken(Base):
    __tablename__ = 'core_mstr_one_qlick_refresh_tokens_tbl'

    refresh_token_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl(user_id)', ondelete='CASCADE'))
    token_hash = Column(String(255), nullable=False)
    expires_at = Column(TIMESTAMP, nullable=False)
    is_revoked = Column(Boolean, default=False)
    device_info = Column(JSONB)
    ip_address = Column(INET)
    user_agent = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

class OAuthProvider(Base):
    __tablename__ = 'core_mstr_one_qlick_oauth_providers_tbl'

    oauth_provider_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl(user_id)', ondelete='CASCADE'))
    provider = Column(Enum(AuthProvider), nullable=False)
    provider_user_id = Column(String(255), nullable=False)
    provider_email = Column(String(255))
    provider_name = Column(String(255))
    provider_photo_url = Column(String(500))
    access_token_hash = Column(String(255))
    refresh_token_hash = Column(String(255))
    token_expires_at = Column(TIMESTAMP)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

class OTPVerification(Base):
    __tablename__ = 'core_mstr_one_qlick_otp_verifications_tbl'

    otp_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl(user_id)', ondelete='CASCADE'))
    phone = Column(String(20))
    email = Column(String(255))
    otp_code = Column(String(10), nullable=False)
    otp_type = Column(Enum(OTPType), nullable=False)
    expires_at = Column(TIMESTAMP, nullable=False)
    is_verified = Column(Boolean, default=False)
    attempts = Column(Integer, default=0)
    max_attempts = Column(Integer, default=3)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

class UserSession(Base):
    __tablename__ = 'core_mstr_one_qlick_user_sessions_tbl'

    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl(user_id)', ondelete='CASCADE'))
    device_id = Column(String(255), nullable=False)
    device_name = Column(String(255))
    device_type = Column(Enum(DeviceType))
    platform = Column(Enum(Platform))
    app_version = Column(String(20))
    is_active = Column(Boolean, default=True)
    last_activity = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

class PasswordResetToken(Base):
    __tablename__ = 'core_mstr_one_qlick_password_reset_tokens_tbl'

    reset_token_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl(user_id)', ondelete='CASCADE'))
    token_hash = Column(String(255), nullable=False)
    expires_at = Column(TIMESTAMP, nullable=False)
    is_used = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
