"""
Razorpay Payment Service
Handles payment order creation, verification, and webhook processing
"""
import razorpay
import hmac
import hashlib
from typing import Dict, Any, Optional
from fastapi import HTTPException, status
import logging
from app.config.config import settings

logger = logging.getLogger(__name__)


class RazorpayService:
    """Service for Razorpay payment gateway integration"""
    
    def __init__(self):
        """Initialize Razorpay client with API credentials"""
        self.client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        self.client.set_app_details({"title": "OneQlick", "version": "1.0.0"})
    
    def create_order(
        self,
        amount: float,
        currency: str = "INR",
        receipt: str = None,
        notes: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Create a Razorpay order
        
        Args:
            amount: Amount in rupees (will be converted to paise)
            currency: Currency code (default: INR)
            receipt: Order receipt ID (optional)
            notes: Additional notes (optional)
        
        Returns:
            Dict containing Razorpay order details
        """
        try:
            # Convert amount to paise (Razorpay uses smallest currency unit)
            amount_in_paise = int(amount * 100)
            
            order_data = {
                "amount": amount_in_paise,
                "currency": currency,
                "payment_capture": 1,  # Auto-capture payment
            }
            
            if receipt:
                order_data["receipt"] = receipt
            
            if notes:
                order_data["notes"] = notes
            
            # Create order via Razorpay API
            razorpay_order = self.client.order.create(data=order_data)
            
            logger.info(f"Razorpay order created: {razorpay_order['id']}")
            
            return {
                "razorpay_order_id": razorpay_order["id"],
                "amount": razorpay_order["amount"],
                "currency": razorpay_order["currency"],
                "status": razorpay_order["status"],
                "created_at": razorpay_order["created_at"]
            }
            
        except razorpay.errors.BadRequestError as e:
            logger.error(f"Razorpay bad request error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid payment request: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Error creating Razorpay order: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create payment order"
            )
    
    def verify_payment_signature(
        self,
        razorpay_order_id: str,
        razorpay_payment_id: str,
        razorpay_signature: str
    ) -> bool:
        """
        Verify Razorpay payment signature for security
        
        Args:
            razorpay_order_id: Razorpay order ID
            razorpay_payment_id: Razorpay payment ID
            razorpay_signature: Signature from Razorpay
        
        Returns:
            True if signature is valid, False otherwise
        """
        try:
            # Create signature string
            message = f"{razorpay_order_id}|{razorpay_payment_id}"
            
            # Generate expected signature
            expected_signature = hmac.new(
                settings.RAZORPAY_KEY_SECRET.encode('utf-8'),
                message.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            # Compare signatures
            is_valid = hmac.compare_digest(expected_signature, razorpay_signature)
            
            if is_valid:
                logger.info(f"Payment signature verified for payment: {razorpay_payment_id}")
            else:
                logger.warning(f"Invalid payment signature for payment: {razorpay_payment_id}")
            
            return is_valid
            
        except Exception as e:
            logger.error(f"Error verifying payment signature: {str(e)}")
            return False
    
    def fetch_payment(self, payment_id: str) -> Dict[str, Any]:
        """
        Fetch payment details from Razorpay
        
        Args:
            payment_id: Razorpay payment ID
        
        Returns:
            Payment details
        """
        try:
            payment = self.client.payment.fetch(payment_id)
            return payment
        except Exception as e:
            logger.error(f"Error fetching payment {payment_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )
    
    def capture_payment(self, payment_id: str, amount: float, currency: str = "INR") -> Dict[str, Any]:
        """
        Manually capture a payment (if auto-capture is disabled)
        
        Args:
            payment_id: Razorpay payment ID
            amount: Amount to capture in rupees
            currency: Currency code
        
        Returns:
            Captured payment details
        """
        try:
            amount_in_paise = int(amount * 100)
            
            captured_payment = self.client.payment.capture(
                payment_id,
                amount_in_paise,
                {"currency": currency}
            )
            
            logger.info(f"Payment captured: {payment_id}")
            return captured_payment
            
        except Exception as e:
            logger.error(f"Error capturing payment {payment_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to capture payment"
            )
    
    def initiate_refund(
        self,
        payment_id: str,
        amount: Optional[float] = None,
        notes: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Initiate a refund for a payment
        
        Args:
            payment_id: Razorpay payment ID
            amount: Amount to refund in rupees (None for full refund)
            notes: Additional notes
        
        Returns:
            Refund details
        """
        try:
            refund_data = {}
            
            if amount is not None:
                refund_data["amount"] = int(amount * 100)
            
            if notes:
                refund_data["notes"] = notes
            
            refund = self.client.payment.refund(payment_id, refund_data)
            
            logger.info(f"Refund initiated for payment {payment_id}: {refund['id']}")
            return refund
            
        except Exception as e:
            logger.error(f"Error initiating refund for payment {payment_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to initiate refund"
            )
    
    def verify_webhook_signature(self, payload: str, signature: str) -> bool:
        """
        Verify webhook signature from Razorpay
        
        Args:
            payload: Webhook payload (raw body)
            signature: X-Razorpay-Signature header
        
        Returns:
            True if signature is valid
        """
        try:
            expected_signature = hmac.new(
                settings.RAZORPAY_WEBHOOK_SECRET.encode('utf-8'),
                payload.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(expected_signature, signature)
            
        except Exception as e:
            logger.error(f"Error verifying webhook signature: {str(e)}")
            return False


# Singleton instance
razorpay_service = RazorpayService()
