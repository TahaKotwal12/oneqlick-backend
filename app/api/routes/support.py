from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional
import math
from app.infra.db.postgres.postgres_config import get_db
from app.api.dependencies import get_current_user, require_admin
from app.infra.db.postgres.models.user import User
from app.services.support_service import SupportService
from app.api.schemas.support_schemas import (
    SupportTicketCreate, 
    SupportTicketResponse, 
    SupportTicketDetailResponse,
    TicketListResponse,
    SupportMessageCreate,
    SupportMessageResponse,
    SupportStatsResponse
)
from app.api.schemas.common_schemas import CommonResponse
from app.utils.enums import TicketStatus, SupportSenderType
from app.config.logger import get_logger
from app.api.routes.websocket import manager

router = APIRouter(prefix="/support", tags=["support"])
logger = get_logger(__name__)

# ============================================
# CUSTOMER SUPPORT ENDPOINTS
# ============================================

@router.post("/tickets", response_model=CommonResponse[SupportTicketResponse])
async def create_ticket(
    ticket_data: SupportTicketCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new support ticket."""
    try:
        ticket = SupportService.create_ticket(db, current_user.user_id, ticket_data)
        return CommonResponse(
            code=status.HTTP_201_CREATED,
            message="Support ticket created successfully",
            message_id="TICKET_CREATED",
            data=SupportTicketResponse.model_validate(ticket)
        )
    except Exception as e:
        logger.error(f"Error creating ticket: {e}")
        raise HTTPException(status_code=500, detail="Failed to create support ticket")

@router.get("/tickets", response_model=CommonResponse[TicketListResponse])
async def get_my_tickets(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get tickets for the current user."""
    tickets, total = SupportService.get_user_tickets(db, current_user.user_id, page, page_size)
    total_pages = math.ceil(total / page_size) if total > 0 else 0
    
    return CommonResponse(
        code=200,
        message="Tickets retrieved successfully",
        message_id="TICKETS_RETRIEVED",
        data=TicketListResponse(
            tickets=[SupportTicketResponse.model_validate(t) for t in tickets],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    )

@router.get("/tickets/{ticket_id}", response_model=CommonResponse[SupportTicketDetailResponse])
async def get_ticket_details(
    ticket_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get ticket details with messages."""
    ticket = SupportService.get_ticket_details(db, ticket_id)
    if not ticket or (ticket.user_id != current_user.user_id and current_user.role != "admin"):
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return CommonResponse(
        code=200,
        message="Ticket details retrieved",
        message_id="TICKET_DETAILS_SUCCESS",
        data=SupportTicketDetailResponse.model_validate(ticket)
    )

@router.post("/tickets/{ticket_id}/messages", response_model=CommonResponse[SupportMessageResponse])
async def send_message(
    ticket_id: UUID,
    message_data: SupportMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message in a ticket and notify via WebSocket."""
    ticket = SupportService.get_ticket_details(db, ticket_id)
    if not ticket or (ticket.user_id != current_user.user_id and current_user.role != "admin"):
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    sender_type = SupportSenderType.ADMIN if current_user.role == "admin" else SupportSenderType.CUSTOMER
    
    message = SupportService.add_message(db, ticket_id, current_user.user_id, sender_type, message_data)
    
    # WebSocket Real-time delivery
    # If admin replies, notify customer. If customer replies, notify admin.
    recipient_id = str(ticket.user_id) if sender_type == SupportSenderType.ADMIN else "ADMIN_BROADCAST"
    
    ws_payload = {
        "type": "support_message",
        "data": SupportMessageResponse.model_validate(message).model_dump(mode="json")
    }
    
    if recipient_id == "ADMIN_BROADCAST":
        # In a real system, we'd have an admin channel. For now, we can broadcast or notify specific connected admins.
        await manager.broadcast(ws_payload) # Simple broadcast for admin demo
    else:
        await manager.send_notification(recipient_id, ws_payload)
        
    return CommonResponse(
        code=201,
        message="Message sent",
        message_id="MESSAGE_SENT",
        data=SupportMessageResponse.model_validate(message)
    )

# ============================================
# ADMIN SUPPORT ENDPOINTS
# ============================================

@router.get("/admin/tickets", response_model=CommonResponse[TicketListResponse])
async def admin_get_tickets(
    status: Optional[TicketStatus] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """List all tickets with filtering (Admin only)."""
    tickets, total = SupportService.get_admin_tickets(db, status, page, page_size)
    total_pages = math.ceil(total / page_size) if total > 0 else 0
    
    return CommonResponse(
        code=200,
        message="All tickets retrieved",
        message_id="ADMIN_TICKETS_SUCCESS",
        data=TicketListResponse(
            tickets=[SupportTicketResponse.model_validate(t) for t in tickets],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    )

@router.patch("/admin/tickets/{ticket_id}/resolve", response_model=CommonResponse)
async def resolve_ticket(
    ticket_id: UUID,
    current_admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Mark ticket as resolved (Admin only)."""
    success = SupportService.resolve_ticket(db, ticket_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ticket not found")
        
    return CommonResponse(
        code=200,
        message="Ticket resolved",
        message_id="TICKET_RESOLVED",
        data={}
    )

@router.get("/admin/stats", response_model=CommonResponse[SupportStatsResponse])
async def get_support_stats(
    current_admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get support dashboard statistics (Admin only)."""
    stats = SupportService.get_support_stats(db)
    return CommonResponse(
        code=200,
        message="Stats retrieved",
        message_id="SUPPORT_STATS_SUCCESS",
        data=SupportStatsResponse(**stats)
    )
