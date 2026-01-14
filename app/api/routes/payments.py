"""
Payment API Routes
Handles payment order creation, verification, and webhook processing
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field
from decimal import Decimal
import logging
import json

from app.infra.db.session import get_db
from app.api.dependencies import get_current_user
from app.infra.db.postgres.models import Payment, Order, User
from app.services.razorpay_service import razorpay_service
from app.utils.enums import PaymentStatus, PaymentMethod, OrderStatus

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/payments", tags=["Payments"])


# Pydantic models for request/response
class CreateOrderRequest(BaseModel):
    """Request to create a payment order"""
    order_id: str = Field(..., description="OneQlick order ID")
    amount: float = Field(..., gt=0, description="Amount in rupees")
    currency: str = Field(default="INR", description="Currency code")


class CreateOrderResponse(BaseModel):
    """Response with Razorpay order details"""
    razorpay_order_id: str
    amount: int  # Amount in paise
    currency: str
    key_id: str  # Razorpay Key ID for frontend


class VerifyPaymentRequest(BaseModel):
    """Request to verify payment"""
    order_id: str
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


class VerifyPaymentResponse(BaseModel):
    """Response after payment verification"""
    verified: bool
    payment_status: str
    order_status: str
    message: str


# Routes
@router.post("/create-order", response_model=CreateOrderResponse)
async def create_payment_order(
    request: CreateOrderRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a Razorpay order for payment
    
    This endpoint is called before opening Razorpay checkout on the frontend.
    It creates a Razorpay order and returns the order ID needed for payment.
    """
    try:
        # Verify order exists and belongs to current user
        order = db.query(Order).filter(
            Order.order_id == request.order_id,
            Order.customer_id == current_user.user_id
        ).first()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # Check if order already has a payment
        existing_payment = db.query(Payment).filter(
            Payment.order_id == request.order_id
        ).first()
        
        if existing_payment and existing_payment.payment_status == PaymentStatus.SUCCESS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order already paid"
            )
        
        # Create Razorpay order
        razorpay_order = razorpay_service.create_order(
            amount=request.amount,
            currency=request.currency,
            receipt=str(request.order_id),
            notes={
                "order_id": str(request.order_id),
                "customer_id": str(current_user.user_id),
                "customer_email": current_user.email
            }
        )
        
        # Create or update payment record
        if existing_payment:
            existing_payment.razorpay_order_id = razorpay_order["razorpay_order_id"]
            existing_payment.amount = request.amount
            existing_payment.currency = request.currency
            existing_payment.payment_status = PaymentStatus.PENDING
        else:
            payment = Payment(
                order_id=request.order_id,
                user_id=current_user.user_id,
                amount=request.amount,
                currency=request.currency,
                payment_method=PaymentMethod.ONLINE,
                payment_status=PaymentStatus.PENDING,
                razorpay_order_id=razorpay_order["razorpay_order_id"]
            )
            db.add(payment)
        
        db.commit()
        
        logger.info(f"Payment order created for order {request.order_id}: {razorpay_order['razorpay_order_id']}")
        
        # Return data needed for frontend Razorpay checkout
        from app.config.config import settings
        return CreateOrderResponse(
            razorpay_order_id=razorpay_order["razorpay_order_id"],
            amount=razorpay_order["amount"],
            currency=razorpay_order["currency"],
            key_id=settings.RAZORPAY_KEY_ID
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating payment order: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create payment order"
        )


@router.post("/verify", response_model=VerifyPaymentResponse)
async def verify_payment(
    request: VerifyPaymentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Verify payment after successful transaction
    
    This endpoint is called after user completes payment on Razorpay checkout.
    It verifies the payment signature and updates order status.
    """
    try:
        # Verify order belongs to current user
        order = db.query(Order).filter(
            Order.order_id == request.order_id,
            Order.customer_id == current_user.user_id
        ).first()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # Get payment record
        payment = db.query(Payment).filter(
            Payment.order_id == request.order_id,
            Payment.razorpay_order_id == request.razorpay_order_id
        ).first()
        
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment record not found"
            )
        
        # Verify payment signature
        is_valid = razorpay_service.verify_payment_signature(
            razorpay_order_id=request.razorpay_order_id,
            razorpay_payment_id=request.razorpay_payment_id,
            razorpay_signature=request.razorpay_signature
        )
        
        if not is_valid:
            payment.payment_status = PaymentStatus.FAILED
            payment.error_description = "Invalid payment signature"
            db.commit()
            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment verification failed"
            )
        
        # Fetch payment details from Razorpay
        razorpay_payment = razorpay_service.fetch_payment(request.razorpay_payment_id)
        
        # Update payment record
        payment.razorpay_payment_id = request.razorpay_payment_id
        payment.razorpay_signature = request.razorpay_signature
        payment.payment_status = PaymentStatus.SUCCESS
        payment.payment_method_details = {
            "method": razorpay_payment.get("method"),
            "vpa": razorpay_payment.get("vpa"),  # UPI ID
            "card_id": razorpay_payment.get("card_id"),
            "wallet": razorpay_payment.get("wallet"),
            "bank": razorpay_payment.get("bank")
        }
        
        # Update order status
        order.payment_status = PaymentStatus.SUCCESS
        order.payment_id = request.razorpay_payment_id
        order.order_status = OrderStatus.CONFIRMED
        
        db.commit()
        
        logger.info(f"Payment verified for order {request.order_id}: {request.razorpay_payment_id}")
        
        return VerifyPaymentResponse(
            verified=True,
            payment_status="success",
            order_status="confirmed",
            message="Payment verified successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error verifying payment: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to verify payment"
        )


@router.post("/webhook")
async def razorpay_webhook(
    request: Request,
    x_razorpay_signature: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Handle Razorpay webhook events
    
    This endpoint receives notifications from Razorpay about payment events.
    Events include: payment.captured, payment.failed, refund.created, etc.
    """
    try:
        # Get raw body for signature verification
        body = await request.body()
        payload = body.decode('utf-8')
        
        # Verify webhook signature
        if not x_razorpay_signature:
            logger.warning("Webhook received without signature")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing signature"
            )
        
        is_valid = razorpay_service.verify_webhook_signature(
            payload=payload,
            signature=x_razorpay_signature
        )
        
        if not is_valid:
            logger.warning("Invalid webhook signature")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid signature"
            )
        
        # Parse webhook data
        webhook_data = json.loads(payload)
        event = webhook_data.get("event")
        payload_data = webhook_data.get("payload", {}).get("payment", {}).get("entity", {})
        
        logger.info(f"Webhook received: {event}")
        
        # Handle different events
        if event == "payment.captured":
            # Payment successful
            payment_id = payload_data.get("id")
            order_id = payload_data.get("notes", {}).get("order_id")
            
            if order_id:
                payment = db.query(Payment).filter(
                    Payment.order_id == order_id
                ).first()
                
                if payment:
                    payment.payment_status = PaymentStatus.SUCCESS
                    payment.razorpay_payment_id = payment_id
                    
                    # Update order
                    order = db.query(Order).filter(Order.order_id == order_id).first()
                    if order:
                        order.payment_status = PaymentStatus.SUCCESS
                        order.order_status = OrderStatus.CONFIRMED
                    
                    db.commit()
                    logger.info(f"Payment captured via webhook: {payment_id}")
        
        elif event == "payment.failed":
            # Payment failed
            payment_id = payload_data.get("id")
            order_id = payload_data.get("notes", {}).get("order_id")
            error_description = payload_data.get("error_description")
            
            if order_id:
                payment = db.query(Payment).filter(
                    Payment.order_id == order_id
                ).first()
                
                if payment:
                    payment.payment_status = PaymentStatus.FAILED
                    payment.error_description = error_description
                    
                    # Update order
                    order = db.query(Order).filter(Order.order_id == order_id).first()
                    if order:
                        order.payment_status = PaymentStatus.FAILED
                    
                    db.commit()
                    logger.info(f"Payment failed via webhook: {payment_id}")
        
        elif event == "refund.created":
            # Refund initiated
            refund_data = webhook_data.get("payload", {}).get("refund", {}).get("entity", {})
            payment_id = refund_data.get("payment_id")
            refund_id = refund_data.get("id")
            refund_amount = refund_data.get("amount", 0) / 100  # Convert paise to rupees
            
            payment = db.query(Payment).filter(
                Payment.razorpay_payment_id == payment_id
            ).first()
            
            if payment:
                payment.is_refunded = True
                payment.refund_id = refund_id
                payment.refund_amount = refund_amount
                payment.refund_status = "processing"
                
                db.commit()
                logger.info(f"Refund created via webhook: {refund_id}")
        
        return {"status": "success", "message": "Webhook processed"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process webhook"
        )
