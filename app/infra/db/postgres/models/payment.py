from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, DECIMAL, Enum, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..base import Base
from app.utils.enums import PaymentStatus, PaymentMethod


class Payment(Base):
    """Payment transactions model."""
    __tablename__ = 'core_mstr_one_qlick_payments_tbl'

    payment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_orders_tbl.order_id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl.user_id'), nullable=False)
    
    # Payment details
    amount = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(3), default='INR', nullable=False)
    payment_method = Column(Enum(PaymentMethod, values_callable=lambda x: [e.value for e in x]), nullable=False)
    payment_status = Column(Enum(PaymentStatus, values_callable=lambda x: [e.value for e in x]), default=PaymentStatus.PENDING, nullable=False)
    
    # Razorpay specific fields
    razorpay_order_id = Column(String(255), unique=True, index=True)  # Razorpay order ID
    razorpay_payment_id = Column(String(255), unique=True, index=True)  # Razorpay payment ID
    razorpay_signature = Column(String(255))  # Signature for verification
    
    # Payment method details (UPI ID, card last 4 digits, etc.)
    payment_method_details = Column(JSON)
    
    # Error handling
    error_code = Column(String(50))
    error_description = Column(String(500))
    error_source = Column(String(100))  # razorpay, gateway, bank
    error_reason = Column(String(255))
    
    # Refund tracking
    is_refunded = Column(Boolean, default=False)
    refund_amount = Column(DECIMAL(10, 2), default=0)
    refund_id = Column(String(255))
    refund_status = Column(String(50))
    refunded_at = Column(TIMESTAMP)
    
    # Metadata
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    
    # Timestamps
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
    paid_at = Column(TIMESTAMP)  # When payment was successful
