from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..base import Base


class UserSession(Base):
    """User sessions model for tracking active sessions."""
    __tablename__ = 'core_mstr_one_qlick_user_sessions_tbl'

    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl(user_id)', ondelete='CASCADE'))
    device_id = Column(String(255), nullable=False)
    device_name = Column(String(255))
    device_type = Column(String(50))  # 'mobile', 'web', 'tablet'
    platform = Column(String(50))  # 'ios', 'android', 'web'
    app_version = Column(String(20))
    is_active = Column(Boolean, default=True)
    last_activity = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'device_id', name='unique_user_device'),
    )
