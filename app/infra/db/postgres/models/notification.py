from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..base import Base
import enum

class NotificationType(str, enum.Enum):
    order_update = 'order_update'
    promotion = 'promotion'
    system = 'system'

class Notification(Base):
    __tablename__ = 'core_mstr_one_qlick_notifications_tbl'

    notification_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl.user_id'))
    title = Column(String(255), nullable=False)
    message = Column(String, nullable=False)
    notification_type = Column(Enum(NotificationType), default=NotificationType.system)
    is_read = Column(Boolean, default=False)
    data_json = Column(String)  # JSONB, but use String for now
    created_at = Column(TIMESTAMP, nullable=False) 