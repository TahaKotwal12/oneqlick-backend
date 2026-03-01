"""
Order service layer for OneQlick food delivery platform.
Contains all business logic for order management.
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from typing import Optional, List, Dict, Any, Tuple
from uuid import UUID
import logging

from app.infra.db.postgres.models.order import Order
from app.infra.db.postgres.models.order_item import OrderItem
from app.infra.db.postgres.models.order_tracking import OrderTracking
from app.infra.db.postgres.models.cart import Cart
from app.infra.db.postgres.models.cart_item import CartItem
from app.infra.db.postgres.models.food_item import FoodItem
from app.infra.db.postgres.models.restaurant import Restaurant
from app.infra.db.postgres.models.address import Address
from app.infra.db.postgres.models.coupon import Coupon
from app.infra.db.postgres.models.user_coupon_usage import UserCouponUsage
from app.infra.db.postgres.models.user import User
from app.utils.order_utils import (
    generate_order_number,
    calculate_distance,
    validate_status_transition,
    is_order_cancellable,
    calculate_estimated_delivery_time,
    calculate_delivery_partner_earnings
)
from app.services.pricing_service import PricingService
from app.services.cart_service import CartService
from app.utils.enums import OrderStatus, PaymentStatus, CouponType, FoodStatus
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)


class OrderService:
    """Service class for order operations"""
    
    @staticmethod
    def validate_and_calculate_order(
        db: Session,
        cart_id: UUID,
        address_id: UUID,
        user_id: UUID,
        coupon_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Validate order and calculate price breakdown.
        
        Args:
            db: Database session
            cart_id: Cart ID
            address_id: Delivery address ID
            user_id: User ID
            coupon_code: Optional coupon code
        
        Returns:
            Dictionary with price breakdown and validation results
        
        Raises:
            HTTPException: If validation fails
        """
        # Get cart
        cart = db.query(Cart).filter(
            Cart.cart_id == cart_id,
            Cart.user_id == user_id
        ).first()
        
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart not found"
            )
        
        # Get cart items
        cart_items = db.query(CartItem).filter(
            CartItem.cart_id == cart_id
        ).all()
        
        if not cart_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart is empty"
            )
        
        # Get restaurant
        restaurant = db.query(Restaurant).filter(
            Restaurant.restaurant_id == cart.restaurant_id
        ).first()
        
        if not restaurant or restaurant.status != 'active':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Restaurant is not available"
            )
        
        # Get delivery address
        address = db.query(Address).filter(
            Address.address_id == address_id,
            Address.user_id == user_id
        ).first()
        
        if not address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Delivery address not found"
            )
        
        # Calculate subtotal and validate items
        subtotal = Decimal('0.00')
        items_data = []
        
        for cart_item in cart_items:
            food_item = db.query(FoodItem).filter(
                FoodItem.food_item_id == cart_item.food_item_id
            ).first()
            
            if not food_item:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Food item not found in cart"
                )
            
            if food_item.status != FoodStatus.AVAILABLE.value:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{food_item.name} is not available"
                )
            
            # Use discount price if available, otherwise regular price
            base_price = food_item.discount_price if food_item.discount_price else food_item.price
            customization_price = CartService.extract_customizations_price(cart_item.special_instructions)
            item_price = base_price + customization_price
            item_total = item_price * cart_item.quantity
            subtotal += item_total
            
            items_data.append({
                'food_item': food_item,
                'cart_item': cart_item,
                'unit_price': item_price,
                'total_price': item_total
            })
        
        # Check minimum order amount
        if restaurant.min_order_amount and subtotal < restaurant.min_order_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Minimum order amount is ₹{restaurant.min_order_amount}"
            )
        
        # Calculate distance
        distance_km = calculate_distance(
            float(address.latitude) if address.latitude else 0,
            float(address.longitude) if address.longitude else 0,
            float(restaurant.latitude),
            float(restaurant.longitude)
        )
        
        # Apply coupon if provided
        discount_amount = Decimal('0.00')
        coupon_applied = None
        
        if coupon_code:
            coupon_result = OrderService._apply_coupon(
                db, coupon_code, subtotal, user_id
            )
            discount_amount = coupon_result['discount_amount']
            coupon_applied = coupon_result['coupon']
        
        # Calculate pricing using PricingService (database-driven)
        delivery_fee = PricingService.calculate_delivery_fee(db, distance_km, subtotal)
        platform_fee = PricingService.calculate_platform_fee(db, subtotal)
        tax_amount = PricingService.calculate_tax(db, subtotal)
        
        # Calculate total
        total_amount = subtotal + tax_amount + delivery_fee + platform_fee - discount_amount
        
        # Ensure total is not negative
        if total_amount < Decimal('0.00'):
            total_amount = Decimal('0.00')
        
        return {
            'cart': cart,
            'cart_items': items_data,
            'restaurant': restaurant,
            'address': address,
            'distance_km': distance_km,
            'subtotal': subtotal,
            'tax_amount': tax_amount,
            'delivery_fee': delivery_fee,
            'platform_fee': platform_fee,
            'discount_amount': discount_amount,
            'total_amount': total_amount,
            'coupon': coupon_applied
        }
    
    @staticmethod
    def _apply_coupon(
        db: Session,
        coupon_code: str,
        subtotal: Decimal,
        user_id: UUID
    ) -> Dict[str, Any]:
        """
        Apply coupon and calculate discount.
        
        Args:
            db: Database session
            coupon_code: Coupon code
            subtotal: Order subtotal
            user_id: User ID
        
        Returns:
            Dictionary with discount amount and coupon object
        
        Raises:
            HTTPException: If coupon is invalid
        """
        # Get coupon
        coupon = db.query(Coupon).filter(
            Coupon.code == coupon_code.upper(),
            Coupon.is_active == True
        ).first()
        
        if not coupon:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid coupon code"
            )
        
        # Check validity period
        now = datetime.now(timezone.utc)
        if now < coupon.valid_from or now > coupon.valid_until:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coupon has expired or not yet valid"
            )
        
        # Check minimum order amount
        if subtotal < coupon.min_order_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Minimum order amount for this coupon is ₹{coupon.min_order_amount}"
            )
        
        # Check usage limit
        if coupon.usage_limit and coupon.used_count >= coupon.usage_limit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coupon usage limit reached"
            )
        
        # Check if user has already used this coupon
        user_usage = db.query(UserCouponUsage).filter(
            UserCouponUsage.user_id == user_id,
            UserCouponUsage.coupon_id == coupon.coupon_id
        ).first()
        
        if user_usage:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already used this coupon"
            )
        
        # Calculate discount
        discount_amount = Decimal('0.00')
        
        if coupon.coupon_type == CouponType.PERCENTAGE:
            discount_amount = subtotal * (coupon.discount_value / Decimal('100'))
            if coupon.max_discount_amount:
                discount_amount = min(discount_amount, coupon.max_discount_amount)
        elif coupon.coupon_type == CouponType.FIXED_AMOUNT:
            discount_amount = coupon.discount_value
        elif coupon.coupon_type == CouponType.FREE_DELIVERY:
            # This will be handled separately in delivery fee calculation
            discount_amount = Decimal('0.00')
        
        return {
            'discount_amount': discount_amount,
            'coupon': coupon
        }
    
    @staticmethod
    def create_order(
        db: Session,
        cart_id: UUID,
        address_id: UUID,
        user_id: UUID,
        payment_method: str,
        coupon_code: Optional[str] = None,
        special_instructions: Optional[str] = None
    ) -> Order:
        """
        Create order from cart.
        
        Args:
            db: Database session
            cart_id: Cart ID
            address_id: Delivery address ID
            user_id: User ID
            payment_method: Payment method
            coupon_code: Optional coupon code
            special_instructions: Optional special instructions
        
        Returns:
            Created order object
        
        Raises:
            HTTPException: If order creation fails
        """
        try:
            # Validate and calculate order
            order_data = OrderService.validate_and_calculate_order(
                db, cart_id, address_id, user_id, coupon_code
            )
            
            # Generate order number
            order_number = generate_order_number()
            
            # Calculate estimated delivery time
            prep_time = order_data['restaurant'].avg_delivery_time or 30
            estimated_delivery_time = calculate_estimated_delivery_time(
                prep_time,
                order_data['distance_km']
            )
            
            # Create order
            order = Order(
                customer_id=user_id,
                restaurant_id=order_data['restaurant'].restaurant_id,
                delivery_address_id=address_id,
                order_number=order_number,
                subtotal=order_data['subtotal'],
                tax_amount=order_data['tax_amount'],
                delivery_fee=order_data['delivery_fee'],
                discount_amount=order_data['discount_amount'],
                total_amount=order_data['total_amount'],
                payment_method=payment_method,
                payment_status=PaymentStatus.PENDING,
                order_status=OrderStatus.PENDING,
                estimated_delivery_time=estimated_delivery_time,
                special_instructions=special_instructions
            )
            
            db.add(order)
            db.flush()  # Get order_id
            
            # Create order items
            for item_data in order_data['cart_items']:
                order_item = OrderItem(
                    order_id=order.order_id,
                    food_item_id=item_data['food_item'].food_item_id,
                    quantity=item_data['cart_item'].quantity,
                    unit_price=item_data['unit_price'],
                    total_price=item_data['total_price'],
                    special_instructions=item_data['cart_item'].special_instructions
                )
                db.add(order_item)
            
            # Create initial order tracking
            tracking = OrderTracking(
                order_id=order.order_id,
                status=OrderStatus.PENDING,
                notes="Order placed successfully"
            )
            db.add(tracking)
            
            # Update coupon usage if applied
            if order_data['coupon']:
                coupon = order_data['coupon']
                coupon.used_count += 1
                
                user_coupon_usage = UserCouponUsage(
                    user_id=user_id,
                    coupon_id=coupon.coupon_id,
                    order_id=order.order_id
                )
                db.add(user_coupon_usage)
            
            # Clear cart
            db.query(CartItem).filter(CartItem.cart_id == cart_id).delete()
            db.query(Cart).filter(Cart.cart_id == cart_id).delete()
            
            db.commit()
            db.refresh(order)
            
            logger.info(f"Order created successfully: {order_number}")
            
            # TODO: Send notification to restaurant
            # TODO: Send confirmation email/SMS to customer
            
            return order
            
        except HTTPException:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating order: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create order: {str(e)}"
            )
    
    @staticmethod
    def cancel_order(
        db: Session,
        order_id: UUID,
        user_id: UUID,
        cancellation_reason: str
    ) -> Order:
        """
        Cancel order.
        
        Args:
            db: Database session
            order_id: Order ID
            user_id: User ID
            cancellation_reason: Reason for cancellation
        
        Returns:
            Updated order object
        
        Raises:
            HTTPException: If cancellation fails
        """
        # Get order
        order = db.query(Order).filter(
            Order.order_id == order_id,
            Order.customer_id == user_id
        ).first()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # Check if order can be cancelled
        can_cancel, reason = is_order_cancellable(order.order_status, order.created_at)
        if not can_cancel:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=reason
            )
        
        # Update order status
        order.order_status = OrderStatus.CANCELLED
        order.cancellation_reason = cancellation_reason
        order.updated_at = datetime.now(timezone.utc)
        
        # Create tracking record
        tracking = OrderTracking(
            order_id=order_id,
            status=OrderStatus.CANCELLED,
            notes=f"Cancelled by customer: {cancellation_reason}"
        )
        db.add(tracking)
        
        # TODO: Process refund if payment was made
        # TODO: Notify restaurant and delivery partner
        
        db.commit()
        db.refresh(order)
        
        logger.info(f"Order cancelled: {order.order_number}")
        
        return order
    
    @staticmethod
    def update_order_status(
        db: Session,
        order_id: UUID,
        new_status: OrderStatus,
        notes: Optional[str] = None
    ) -> Order:
        """
        Update order status.
        
        Args:
            db: Database session
            order_id: Order ID
            new_status: New order status
            notes: Optional notes
        
        Returns:
            Updated order object
        
        Raises:
            HTTPException: If status update fails
        """
        # Get order
        order = db.query(Order).filter(Order.order_id == order_id).first()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # Validate status transition
        if not validate_status_transition(order.order_status, new_status):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot transition from {order.order_status.value} to {new_status.value}"
            )
        
        # Update order status
        order.order_status = new_status
        order.updated_at = datetime.now(timezone.utc)
        
        # Set delivery time if delivered
        if new_status == OrderStatus.DELIVERED:
            order.actual_delivery_time = datetime.now(timezone.utc)
        
        # Create tracking record
        tracking = OrderTracking(
            order_id=order_id,
            status=new_status,
            notes=notes
        )
        db.add(tracking)
        
        db.commit()
        db.refresh(order)
        
        logger.info(f"Order status updated: {order.order_number} -> {new_status.value}")
        
        # TODO: Send notification to customer
        
        return order
