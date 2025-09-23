from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..base import Base


class OTPVerification(Base):
    """OTP verification model for phone/email verification."""
    __tablename__ = 'core_mstr_one_qlick_otp_verifications_tbl'

    otp_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl(user_id)', ondelete='CASCADE'))
    phone = Column(String(20))
    email = Column(String(255))
    otp_code = Column(String(10), nullable=False)
    otp_type = Column(String(20), nullable=False)  # 'phone_verification', 'email_verification', 'password_reset'
    expires_at = Column(TIMESTAMP, nullable=False)
    is_verified = Column(Boolean, default=False)
    attempts = Column(Integer, default=0)
    max_attempts = Column(Integer, default=3)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
