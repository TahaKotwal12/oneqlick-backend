from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from app.utils.enums import TicketCategory, TicketStatus, TicketPriority, SupportSenderType

# Message Schemas
class SupportMessageBase(BaseModel):
    content: str
    attachment_url: Optional[str] = None

class SupportMessageCreate(SupportMessageBase):
    pass

class SupportMessageResponse(SupportMessageBase):
    message_id: UUID
    ticket_id: UUID
    sender_id: UUID
    sender_type: SupportSenderType
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Ticket Schemas
class SupportTicketBase(BaseModel):
    subject: str
    category: TicketCategory
    priority: TicketPriority = TicketPriority.MEDIUM
    order_id: Optional[UUID] = None

class SupportTicketCreate(SupportTicketBase):
    initial_message: str

class SupportTicketResponse(SupportTicketBase):
    ticket_id: UUID
    user_id: UUID
    status: TicketStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SupportTicketDetailResponse(SupportTicketResponse):
    messages: List[SupportMessageResponse] = []

class TicketListResponse(BaseModel):
    tickets: List[SupportTicketResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

class SupportStatsResponse(BaseModel):
    total_tickets: int
    open_tickets: int
    in_progress_tickets: int
    resolved_tickets: int
    tickets_by_category: dict
    avg_resolution_time: Optional[float] = None # In hours
