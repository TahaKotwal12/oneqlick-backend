from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey, INET
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from ..base import Base


class RefreshToken(Base):
    """Refresh tokens model for JWT refresh mechanism."""
    __tablename__ = 'core_mstr_one_qlick_refresh_tokens_tbl'

    refresh_token_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl(user_id)', ondelete='CASCADE'))
    token_hash = Column(String(255), nullable=False)
    expires_at = Column(TIMESTAMP, nullable=False)
    is_revoked = Column(Boolean, default=False)
    device_info = Column(JSONB)  # Store device fingerprint for security
    ip_address = Column(INET)
    user_agent = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
