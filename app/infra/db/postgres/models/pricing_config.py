from sqlalchemy import Column, String, Numeric, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid

from ..base import Base


class PricingConfig(Base):
    """
    Pricing configuration table for dynamic pricing rules.
    Allows admins to configure pricing without code changes.
    """
    __tablename__ = "core_mstr_one_qlick_pricing_config_tbl"

    config_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    config_key = Column(String(100), unique=True, nullable=False, index=True)
    config_value = Column(Numeric(10, 2), nullable=False)
    config_type = Column(String(50), nullable=False)  # 'percentage', 'fixed', 'threshold'
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<PricingConfig(key={self.config_key}, value={self.config_value}, type={self.config_type})>"
