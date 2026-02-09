from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from ..base import Base
from app.utils.enums import NotificationType


class Notification(Base):
    """Notifications model."""
    __tablename__ = 'core_mstr_one_qlick_notifications_tbl'

    notification_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl.user_id'))
    title = Column(String(255), nullable=False)
    message = Column(String, nullable=False)
    notification_type = Column(Enum(NotificationType, values_callable=lambda x: [e.value for e in x]), default=NotificationType.SYSTEM_ANNOUNCEMENT)
    is_read = Column(Boolean, default=False)
    data_json = Column(JSONB)  # Additional data
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
