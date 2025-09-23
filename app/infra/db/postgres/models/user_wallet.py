from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..base import Base


class UserWallet(Base):
    """User wallet model."""
    __tablename__ = 'core_mstr_one_qlick_user_wallets_tbl'

    wallet_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl(user_id)', ondelete='CASCADE'))
    balance = Column(DECIMAL(10, 2), default=0)
    currency = Column(String(3), default='INR')
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
