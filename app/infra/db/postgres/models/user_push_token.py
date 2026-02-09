from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base

class UserPushToken(Base):
    """Model for storing user push notification tokens"""
    __tablename__ = "core_mstr_one_qlick_user_push_tokens_tbl"

    token_id = Column(UUID, primary_key=True, server_default="gen_random_uuid()")
    user_id = Column(UUID, ForeignKey("core_mstr_one_qlick_users_tbl.user_id", ondelete="CASCADE"), nullable=False)
    push_token = Column(String, nullable=False, unique=True)
    device_type = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationship to User
    user = relationship("User", back_populates="push_tokens")

    __table_args__ = (
        CheckConstraint("device_type IN ('ios', 'android')", name="check_device_type"),
    )

    def __repr__(self):
        return f"<UserPushToken(token_id={self.token_id}, user_id={self.user_id}, device_type={self.device_type})>"
