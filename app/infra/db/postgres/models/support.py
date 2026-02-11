from sqlalchemy import Column, String, Text, Boolean, TIMESTAMP, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from ..base import Base
from app.utils.enums import TicketCategory, TicketStatus, TicketPriority, SupportSenderType

class SupportTicket(Base):
    __tablename__ = "core_mstr_one_qlick_support_tickets_tbl"

    ticket_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("core_mstr_one_qlick_users_tbl.user_id"), nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey("core_mstr_one_qlick_orders_tbl.order_id"), nullable=True)
    subject = Column(String(255), nullable=False)
    category = Column(SQLEnum(TicketCategory, values_callable=lambda x: [e.value for e in x]), nullable=False, default=TicketCategory.OTHER)
    status = Column(SQLEnum(TicketStatus, values_callable=lambda x: [e.value for e in x]), nullable=False, default=TicketStatus.OPEN)
    priority = Column(SQLEnum(TicketPriority, values_callable=lambda x: [e.value for e in x]), nullable=False, default=TicketPriority.MEDIUM)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", backref="support_tickets")
    order = relationship("Order", backref="support_tickets")
    messages = relationship("SupportMessage", back_populates="ticket", cascade="all, delete-orphan")

class SupportMessage(Base):
    __tablename__ = "core_mstr_one_qlick_support_messages_tbl"

    message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("core_mstr_one_qlick_support_tickets_tbl.ticket_id"), nullable=False)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("core_mstr_one_qlick_users_tbl.user_id"), nullable=False)
    sender_type = Column(SQLEnum(SupportSenderType, values_callable=lambda x: [e.value for e in x]), nullable=False)
    content = Column(Text, nullable=False)
    attachment_url = Column(String(512), nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    # Relationships
    ticket = relationship("SupportTicket", back_populates="messages")
    sender = relationship("User")
