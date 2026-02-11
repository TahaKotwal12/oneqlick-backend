from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Tuple, Optional
from uuid import UUID
from datetime import datetime, timedelta
from app.infra.db.postgres.models.support import SupportTicket, SupportMessage
from app.utils.enums import TicketStatus, SupportSenderType
from app.api.schemas.support_schemas import SupportTicketCreate, SupportMessageCreate
from app.config.logger import get_logger

logger = get_logger(__name__)

class SupportService:
    @staticmethod
    def create_ticket(db: Session, user_id: UUID, ticket_data: SupportTicketCreate) -> SupportTicket:
        """Create a new support ticket with an initial message."""
        ticket = SupportTicket(
            user_id=user_id,
            order_id=ticket_data.order_id,
            subject=ticket_data.subject,
            category=ticket_data.category,
            priority=ticket_data.priority,
            status=TicketStatus.OPEN
        )
        db.add(ticket)
        db.flush()  # Get ticket_id

        initial_message = SupportMessage(
            ticket_id=ticket.ticket_id,
            sender_id=user_id,
            sender_type=SupportSenderType.CUSTOMER,
            content=ticket_data.initial_message
        )
        db.add(initial_message)
        db.commit()
        db.refresh(ticket)
        return ticket

    @staticmethod
    def get_user_tickets(db: Session, user_id: UUID, page: int = 1, page_size: int = 20) -> Tuple[List[SupportTicket], int]:
        """Get paginated tickets for a specific user."""
        query = db.query(SupportTicket).filter(SupportTicket.user_id == user_id)
        total = query.count()
        tickets = query.order_by(SupportTicket.updated_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
        return tickets, total

    @staticmethod
    def get_admin_tickets(
        db: Session, 
        status: Optional[TicketStatus] = None, 
        page: int = 1, 
        page_size: int = 20
    ) -> Tuple[List[SupportTicket], int]:
        """Get all tickets for admin with optional status filter."""
        query = db.query(SupportTicket)
        if status:
            query = query.filter(SupportTicket.status == status)
        
        total = query.count()
        tickets = query.order_by(SupportTicket.updated_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
        return tickets, total

    @staticmethod
    def get_ticket_details(db: Session, ticket_id: UUID) -> Optional[SupportTicket]:
        """Get ticket with all messages."""
        return db.query(SupportTicket).filter(SupportTicket.ticket_id == ticket_id).first()

    @staticmethod
    def add_message(
        db: Session, 
        ticket_id: UUID, 
        sender_id: UUID, 
        sender_type: SupportSenderType, 
        message_data: SupportMessageCreate
    ) -> SupportMessage:
        """Add a message to an existing ticket and update ticket status."""
        message = SupportMessage(
            ticket_id=ticket_id,
            sender_id=sender_id,
            sender_type=sender_type,
            content=message_data.content,
            attachment_url=message_data.attachment_url
        )
        db.add(message)
        
        # Update ticket's updated_at and move to IN_PROGRESS if admin replies
        ticket = db.query(SupportTicket).filter(SupportTicket.ticket_id == ticket_id).first()
        if ticket:
            ticket.updated_at = datetime.utcnow()
            if sender_type == SupportSenderType.ADMIN and ticket.status == TicketStatus.OPEN:
                ticket.status = TicketStatus.IN_PROGRESS
        
        db.commit()
        db.refresh(message)
        return message

    @staticmethod
    def resolve_ticket(db: Session, ticket_id: UUID) -> bool:
        """Mark a ticket as resolved."""
        ticket = db.query(SupportTicket).filter(SupportTicket.ticket_id == ticket_id).first()
        if ticket:
            ticket.status = TicketStatus.RESOLVED
            ticket.updated_at = datetime.utcnow()
            db.commit()
            return True
        return False

    @staticmethod
    def get_support_stats(db: Session) -> dict:
        """Get support statistics for admin dashboard."""
        total = db.query(SupportTicket).count()
        open_count = db.query(SupportTicket).filter(SupportTicket.status == TicketStatus.OPEN).count()
        in_progress = db.query(SupportTicket).filter(SupportTicket.status == TicketStatus.IN_PROGRESS).count()
        resolved = db.query(SupportTicket).filter(SupportTicket.status == TicketStatus.RESOLVED).count()
        
        # Breakdown by category
        categories = db.query(SupportTicket.category, func.count(SupportTicket.ticket_id)).group_by(SupportTicket.category).all()
        cat_breakdown = {cat.value: count for cat, count in categories}
        
        return {
            "total_tickets": total,
            "open_tickets": open_count,
            "in_progress_tickets": in_progress,
            "resolved_tickets": resolved,
            "tickets_by_category": cat_breakdown
        }
