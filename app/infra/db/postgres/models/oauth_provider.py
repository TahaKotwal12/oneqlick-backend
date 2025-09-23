from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..base import Base


class OAuthProvider(Base):
    """OAuth providers model for social login."""
    __tablename__ = 'core_mstr_one_qlick_oauth_providers_tbl'

    oauth_provider_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl(user_id)', ondelete='CASCADE'))
    provider = Column(String(50), nullable=False)  # 'google', 'facebook', 'apple'
    provider_user_id = Column(String(255), nullable=False)
    provider_email = Column(String(255))
    provider_name = Column(String(255))
    provider_photo_url = Column(String(500))
    access_token_hash = Column(String(255))  # Encrypted access token
    refresh_token_hash = Column(String(255))  # Encrypted refresh token
    token_expires_at = Column(TIMESTAMP)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('provider', 'provider_user_id', name='unique_provider_user'),
    )
