"""
Order management routes for OneQlick food delivery platform.
Handles all order-related operations for customers, restaurants, delivery partners, and admins.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from typing import Optional, List
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from uuid import UUID

from app.infra.db.postgres.postgres_config import get_db
from app.api.dependencies import get_current_user, get_optional_current_user
from app.api.schemas.order_schemas import *
from app.api.schemas.common_schemas import CommonResponse
from app.services.order_service import OrderService
from app.infra.db.postgres.models.order import Order
from app.infra.db.postgres.models.order_item import OrderItem
from app.infra.db.postgres.models.order_tracking import OrderTracking
from app.infra.db.postgres.models.user import User
from app.infra.db.postgres.models.restaurant import Restaurant
from app.infra.db.postgres.models.address import Address
from app.infra.db.postgres.models.food_item import FoodItem
from app.infra.db.postgres.models.delivery_partner import DeliveryPartner
from app.utils.enums import OrderStatus, PaymentStatus, UserRole
from app.utils.order_utils import (
    calculate_distance,
    is_order_ratable,
    calculate_delivery_partner_earnings
)
from app.config.logger import get_logger

router = APIRouter(prefix="/orders", tags=["orders"])
logger = get_logger(__name__)


# ============================================
# CUSTOMER ORDER APIS
# ============================================

@router.post("/create", response_model=CommonResponse[OrderResponse], status_code=201)
async def create_order(
    request: OrderCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create order from cart.
    
    This endpoint:
    1. Validates cart and items
    2. Calculates prices and applies coupon
    3. Creates order and order items
    4. Clears cart
    5. Sends notification to restaurant
    """
    try:
        logger.info(f"Creating order for user {current_user.user_id} from cart {request.cart_id}")
        
        # Create order using service
        order = OrderService.create_order(
            db=db,
            cart_id=request.cart_id,
            address_id=request.address_id,
            user_id=current_user.user_id,
            payment_method=request.payment_method.value,
            coupon_code=request.coupon_code,
            special_instructions=request.special_instructions
        )
        
        # Fetch complete order data for response
        restaurant = db.query(Restaurant).filter(
            Restaurant.restaurant_id == order.restaurant_id
        ).first()
        
        address = db.query(Address).filter(
            Address.address_id == order.delivery_address_id
        ).first()
        
        # Build response
        restaurant_response = RestaurantBasicResponse(
            restaurant_id=restaurant.restaurant_id,
            name=restaurant.name,
            phone=restaurant.phone,
            image=restaurant.image,
            address_line1=restaurant.address_line1,
            city=restaurant.city
        )
        
        address_response = AddressResponse(
            address_id=address.address_id,
            title=address.title,
            address_line1=address.address_line1,
            address_line2=address.address_line2,
            city=address.city,
            state=address.state,
            postal_code=address.postal_code,
            latitude=address.latitude,
            longitude=address.longitude
        )
        
        order_response = OrderResponse(
            order_id=order.order_id,
            order_number=order.order_number,
            customer_id=order.customer_id,
            restaurant_id=order.restaurant_id,
            restaurant=restaurant_response,
            delivery_partner_id=order.delivery_partner_id,
            delivery_address_id=order.delivery_address_id,
            delivery_address=address_response,
            subtotal=order.subtotal,
            tax_amount=order.tax_amount,
            delivery_fee=order.delivery_fee,
            discount_amount=order.discount_amount,
            total_amount=order.total_amount,
            payment_method=order.payment_method,
            payment_status=order.payment_status,
            payment_id=order.payment_id,
            order_status=order.order_status,
            estimated_delivery_time=order.estimated_delivery_time,
            actual_delivery_time=order.actual_delivery_time,
            special_instructions=order.special_instructions,
            cancellation_reason=order.cancellation_reason,
            rating=order.rating,
            review=order.review,
            created_at=order.created_at,
            updated_at=order.updated_at
        )
        
        return CommonResponse(
            code=201,
            message="Order created successfully",
            message_id="ORDER_CREATED",
            data=order_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create order: {str(e)}"
        )


@router.post("/validate", response_model=CommonResponse[PriceBreakdownResponse])
async def validate_order(
    request: OrderValidateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Validate order and get price breakdown before placing order.
    
    This endpoint calculates:
    - Subtotal
    - Tax
    - Delivery fee
    - Discount (if coupon applied)
    - Total amount
    """
    try:
        logger.info(f"Validating order for user {current_user.user_id}")
        
        # Validate and calculate
        order_data = OrderService.validate_and_calculate_order(
            db=db,
            cart_id=request.cart_id,
            address_id=request.address_id,
            user_id=current_user.user_id,
            coupon_code=request.coupon_code
        )
        
        # Build price breakdown response
        price_breakdown = PriceBreakdownResponse(
            subtotal=order_data['subtotal'],
            tax_amount=order_data['tax_amount'],
            delivery_fee=order_data['delivery_fee'],
            discount_amount=order_data['discount_amount'],
            platform_fee=order_data['platform_fee'],
            total_amount=order_data['total_amount'],
            coupon_applied=order_data['coupon'].code if order_data['coupon'] else None,
            coupon_discount=order_data['discount_amount'] if order_data['coupon'] else None
        )
        
        return CommonResponse(
            code=200,
            message="Order validated successfully",
            message_id="ORDER_VALIDATED",
            data=price_breakdown
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating order: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to validate order: {str(e)}"
        )


@router.get("/my-orders", response_model=CommonResponse[MyOrdersResponse])
async def get_my_orders(
    status_filter: Optional[OrderStatus] = Query(None, description="Filter by order status"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=50, description="Items per page"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's order history with pagination and filtering.
    """
    try:
        logger.info(f"Fetching orders for user {current_user.user_id}")
        
        # Build query
        query = db.query(Order).filter(Order.customer_id == current_user.user_id)
        
        # Apply status filter
        if status_filter:
            query = query.filter(Order.order_status == status_filter)
        
        # Get total count
        total_count = query.count()
        
        # Apply pagination and ordering
        offset = (page - 1) * limit
        orders = query.order_by(desc(Order.created_at)).offset(offset).limit(limit).all()
        
        # Build response
        order_responses = []
        for order in orders:
            restaurant = db.query(Restaurant).filter(
                Restaurant.restaurant_id == order.restaurant_id
            ).first()
            
            address = db.query(Address).filter(
                Address.address_id == order.delivery_address_id
            ).first()
            
            restaurant_response = RestaurantBasicResponse(
                restaurant_id=restaurant.restaurant_id,
                name=restaurant.name,
                phone=restaurant.phone,
                image=restaurant.image,
                address_line1=restaurant.address_line1,
                city=restaurant.city
            )
            
            address_response = AddressResponse(
                address_id=address.address_id,
                title=address.title,
                address_line1=address.address_line1,
                address_line2=address.address_line2,
                city=address.city,
                state=address.state,
                postal_code=address.postal_code,
                latitude=address.latitude,
                longitude=address.longitude
            )
            
            order_response = OrderResponse(
                order_id=order.order_id,
                order_number=order.order_number,
                customer_id=order.customer_id,
                restaurant_id=order.restaurant_id,
                restaurant=restaurant_response,
                delivery_partner_id=order.delivery_partner_id,
                delivery_address_id=order.delivery_address_id,
                delivery_address=address_response,
                subtotal=order.subtotal,
                tax_amount=order.tax_amount,
                delivery_fee=order.delivery_fee,
                discount_amount=order.discount_amount,
                total_amount=order.total_amount,
                payment_method=order.payment_method,
                payment_status=order.payment_status,
                payment_id=order.payment_id,
                order_status=order.order_status,
                estimated_delivery_time=order.estimated_delivery_time,
                actual_delivery_time=order.actual_delivery_time,
                special_instructions=order.special_instructions,
                cancellation_reason=order.cancellation_reason,
                rating=order.rating,
                review=order.review,
                created_at=order.created_at,
                updated_at=order.updated_at
            )
            
            order_responses.append(order_response)
        
        has_more = (offset + limit) < total_count
        
        return CommonResponse(
            code=200,
            message=f"Found {len(order_responses)} orders",
            message_id="ORDERS_RETRIEVED",
            data=MyOrdersResponse(
                orders=order_responses,
                total_count=total_count,
                has_more=has_more
            )
        )
        
    except Exception as e:
        logger.error(f"Error fetching orders: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch orders: {str(e)}"
        )


@router.get("/{order_id}", response_model=CommonResponse[OrderDetailResponse])
async def get_order_details(
    order_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get complete order details including items, tracking, and delivery partner info.
    """
    try:
        # Get order
        order = db.query(Order).filter(
            Order.order_id == order_id,
            Order.customer_id == current_user.user_id
        ).first()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # Get order items
        order_items = db.query(OrderItem).filter(
            OrderItem.order_id == order_id
        ).all()
        
        # Get tracking history
        tracking_history = db.query(OrderTracking).filter(
            OrderTracking.order_id == order_id
        ).order_by(OrderTracking.created_at).all()
        
        # Get restaurant
        restaurant = db.query(Restaurant).filter(
            Restaurant.restaurant_id == order.restaurant_id
        ).first()
        
        # Get address
        address = db.query(Address).filter(
            Address.address_id == order.delivery_address_id
        ).first()
        
        # Get delivery partner if assigned
        delivery_partner_response = None
        if order.delivery_partner_id:
            delivery_partner_user = db.query(User).filter(
                User.user_id == order.delivery_partner_id
            ).first()
            
            delivery_partner = db.query(DeliveryPartner).filter(
                DeliveryPartner.user_id == order.delivery_partner_id
            ).first()
            
            if delivery_partner_user and delivery_partner:
                delivery_partner_response = DeliveryPartnerResponse(
                    user_id=delivery_partner_user.user_id,
                    first_name=delivery_partner_user.first_name,
                    last_name=delivery_partner_user.last_name,
                    phone=delivery_partner_user.phone,
                    profile_image=delivery_partner_user.profile_image,
                    vehicle_type=delivery_partner.vehicle_type.value if delivery_partner.vehicle_type else None,
                    vehicle_number=delivery_partner.vehicle_number,
                    rating=delivery_partner.rating
                )
        
        # Build item responses
        item_responses = []
        for item in order_items:
            food_item = db.query(FoodItem).filter(
                FoodItem.food_item_id == item.food_item_id
            ).first()
            
            item_response = OrderItemResponse(
                order_item_id=item.order_item_id,
                food_item_id=item.food_item_id,
                food_item_name=food_item.name if food_item else "Unknown",
                food_item_image=food_item.image if food_item else None,
                variant_id=item.variant_id,
                variant_name=None,  # TODO: Get variant name
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item.total_price,
                special_instructions=item.special_instructions,
                is_veg=food_item.is_veg if food_item else True
            )
            item_responses.append(item_response)
        
        # Build tracking responses
        tracking_responses = [
            OrderTrackingResponse(
                order_tracking_id=t.order_tracking_id,
                status=t.status,
                latitude=t.latitude,
                longitude=t.longitude,
                notes=t.notes,
                created_at=t.created_at
            ) for t in tracking_history
        ]
        
        # Build complete response
        order_detail = OrderDetailResponse(
            order_id=order.order_id,
            order_number=order.order_number,
            customer_id=order.customer_id,
            restaurant_id=order.restaurant_id,
            restaurant=RestaurantBasicResponse(
                restaurant_id=restaurant.restaurant_id,
                name=restaurant.name,
                phone=restaurant.phone,
                image=restaurant.image,
                address_line1=restaurant.address_line1,
                city=restaurant.city
            ),
            delivery_partner_id=order.delivery_partner_id,
            delivery_address_id=order.delivery_address_id,
            delivery_address=AddressResponse(
                address_id=address.address_id,
                title=address.title,
                address_line1=address.address_line1,
                address_line2=address.address_line2,
                city=address.city,
                state=address.state,
                postal_code=address.postal_code,
                latitude=address.latitude,
                longitude=address.longitude
            ),
            subtotal=order.subtotal,
            tax_amount=order.tax_amount,
            delivery_fee=order.delivery_fee,
            discount_amount=order.discount_amount,
            total_amount=order.total_amount,
            payment_method=order.payment_method,
            payment_status=order.payment_status,
            payment_id=order.payment_id,
            order_status=order.order_status,
            estimated_delivery_time=order.estimated_delivery_time,
            actual_delivery_time=order.actual_delivery_time,
            special_instructions=order.special_instructions,
            cancellation_reason=order.cancellation_reason,
            rating=order.rating,
            review=order.review,
            created_at=order.created_at,
            updated_at=order.updated_at,
            items=item_responses,
            delivery_partner=delivery_partner_response,
            tracking=tracking_responses
        )
        
        return CommonResponse(
            code=200,
            message="Order details retrieved successfully",
            message_id="ORDER_DETAILS_RETRIEVED",
            data=order_detail
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching order details: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch order details: {str(e)}"
        )


@router.post("/{order_id}/cancel", response_model=CommonResponse[OrderResponse])
async def cancel_order(
    order_id: UUID,
    request: OrderCancelRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cancel order.
    
    Orders can only be cancelled if:
    - Status is pending, confirmed, or preparing
    - Not already picked up by delivery partner
    """
    try:
        logger.info(f"Cancelling order {order_id} for user {current_user.user_id}")
        
        # Cancel order using service
        order = OrderService.cancel_order(
            db=db,
            order_id=order_id,
            user_id=current_user.user_id,
            cancellation_reason=request.cancellation_reason
        )
        
        # Get related data for response
        restaurant = db.query(Restaurant).filter(
            Restaurant.restaurant_id == order.restaurant_id
        ).first()
        
        address = db.query(Address).filter(
            Address.address_id == order.delivery_address_id
        ).first()
        
        # Build response (similar to create_order)
        order_response = OrderResponse(
            order_id=order.order_id,
            order_number=order.order_number,
            customer_id=order.customer_id,
            restaurant_id=order.restaurant_id,
            restaurant=RestaurantBasicResponse(
                restaurant_id=restaurant.restaurant_id,
                name=restaurant.name,
                phone=restaurant.phone,
                image=restaurant.image,
                address_line1=restaurant.address_line1,
                city=restaurant.city
            ),
            delivery_partner_id=order.delivery_partner_id,
            delivery_address_id=order.delivery_address_id,
            delivery_address=AddressResponse(
                address_id=address.address_id,
                title=address.title,
                address_line1=address.address_line1,
                address_line2=address.address_line2,
                city=address.city,
                state=address.state,
                postal_code=address.postal_code,
                latitude=address.latitude,
                longitude=address.longitude
            ),
            subtotal=order.subtotal,
            tax_amount=order.tax_amount,
            delivery_fee=order.delivery_fee,
            discount_amount=order.discount_amount,
            total_amount=order.total_amount,
            payment_method=order.payment_method,
            payment_status=order.payment_status,
            payment_id=order.payment_id,
            order_status=order.order_status,
            estimated_delivery_time=order.estimated_delivery_time,
            actual_delivery_time=order.actual_delivery_time,
            special_instructions=order.special_instructions,
            cancellation_reason=order.cancellation_reason,
            rating=order.rating,
            review=order.review,
            created_at=order.created_at,
            updated_at=order.updated_at
        )
        
        return CommonResponse(
            code=200,
            message="Order cancelled successfully",
            message_id="ORDER_CANCELLED",
            data=order_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cancelling order: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel order: {str(e)}"
        )


@router.post("/{order_id}/rate", response_model=CommonResponse[dict])
async def rate_order(
    order_id: UUID,
    request: OrderRatingRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Rate order after delivery.
    
    Can rate:
    - Restaurant (required)
    - Delivery partner (optional)
    - Individual food items (optional)
    """
    try:
        # Get order
        order = db.query(Order).filter(
            Order.order_id == order_id,
            Order.customer_id == current_user.user_id
        ).first()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # Check if order can be rated
        can_rate, reason = is_order_ratable(order.order_status, order.actual_delivery_time)
        if not can_rate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=reason
            )
        
        # Update order rating
        order.rating = request.restaurant_rating
        order.review = request.review_text
        order.updated_at = datetime.now(timezone.utc)
        
        # Update restaurant rating
        restaurant = db.query(Restaurant).filter(
            Restaurant.restaurant_id == order.restaurant_id
        ).first()
        
        if restaurant:
            # Recalculate average rating
            total_ratings = restaurant.total_ratings or 0
            current_avg = float(restaurant.rating or 0)
            new_avg = ((current_avg * total_ratings) + request.restaurant_rating) / (total_ratings + 1)
            
            restaurant.rating = Decimal(str(round(new_avg, 2)))
            restaurant.total_ratings = total_ratings + 1
        
        # Update delivery partner rating if provided
        if request.delivery_rating and order.delivery_partner_id:
            delivery_partner = db.query(DeliveryPartner).filter(
                DeliveryPartner.user_id == order.delivery_partner_id
            ).first()
            
            if delivery_partner:
                total_ratings = delivery_partner.total_ratings or 0
                current_avg = float(delivery_partner.rating or 0)
                new_avg = ((current_avg * total_ratings) + request.delivery_rating) / (total_ratings + 1)
                
                delivery_partner.rating = Decimal(str(round(new_avg, 2)))
                delivery_partner.total_ratings = total_ratings + 1
        
        db.commit()
        
        logger.info(f"Order {order.order_number} rated successfully")
        
        return CommonResponse(
            code=200,
            message="Order rated successfully",
            message_id="ORDER_RATED",
            data={"order_id": str(order_id), "rating": request.restaurant_rating}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error rating order: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to rate order: {str(e)}"
        )


@router.get("/{order_id}/track", response_model=CommonResponse[OrderTrackingDetailResponse])
async def track_order(
    order_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get real-time order tracking information.
    
    Returns:
    - Current order status
    - Delivery partner location (if assigned)
    - Tracking history
    - Estimated delivery time
    """
    try:
        # Get order
        order = db.query(Order).filter(
            Order.order_id == order_id,
            Order.customer_id == current_user.user_id
        ).first()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # Get tracking history
        tracking_history = db.query(OrderTracking).filter(
            OrderTracking.order_id == order_id
        ).order_by(OrderTracking.created_at).all()
        
        # Get restaurant
        restaurant = db.query(Restaurant).filter(
            Restaurant.restaurant_id == order.restaurant_id
        ).first()
        
        # Get address
        address = db.query(Address).filter(
            Address.address_id == order.delivery_address_id
        ).first()
        
        # Get delivery partner location if assigned
        current_location = None
        delivery_partner_response = None
        
        if order.delivery_partner_id:
            delivery_partner_user = db.query(User).filter(
                User.user_id == order.delivery_partner_id
            ).first()
            
            delivery_partner = db.query(DeliveryPartner).filter(
                DeliveryPartner.user_id == order.delivery_partner_id
            ).first()
            
            if delivery_partner_user and delivery_partner:
                delivery_partner_response = DeliveryPartnerResponse(
                    user_id=delivery_partner_user.user_id,
                    first_name=delivery_partner_user.first_name,
                    last_name=delivery_partner_user.last_name,
                    phone=delivery_partner_user.phone,
                    profile_image=delivery_partner_user.profile_image,
                    vehicle_type=delivery_partner.vehicle_type.value if delivery_partner.vehicle_type else None,
                    vehicle_number=delivery_partner.vehicle_number,
                    rating=delivery_partner.rating
                )
                
                # Get current location
                if delivery_partner.current_latitude and delivery_partner.current_longitude:
                    current_location = {
                        "latitude": float(delivery_partner.current_latitude),
                        "longitude": float(delivery_partner.current_longitude)
                    }
        
        # Build tracking responses
        tracking_responses = [
            OrderTrackingResponse(
                order_tracking_id=t.order_tracking_id,
                status=t.status,
                latitude=t.latitude,
                longitude=t.longitude,
                notes=t.notes,
                created_at=t.created_at
            ) for t in tracking_history
        ]
        
        # Build tracking detail response
        tracking_detail = OrderTrackingDetailResponse(
            order_id=order.order_id,
            order_number=order.order_number,
            order_status=order.order_status,
            estimated_delivery_time=order.estimated_delivery_time,
            restaurant=RestaurantBasicResponse(
                restaurant_id=restaurant.restaurant_id,
                name=restaurant.name,
                phone=restaurant.phone,
                image=restaurant.image,
                address_line1=restaurant.address_line1,
                city=restaurant.city
            ),
            delivery_address=AddressResponse(
                address_id=address.address_id,
                title=address.title,
                address_line1=address.address_line1,
                address_line2=address.address_line2,
                city=address.city,
                state=address.state,
                postal_code=address.postal_code,
                latitude=address.latitude,
                longitude=address.longitude
            ),
            delivery_partner=delivery_partner_response,
            current_location=current_location,
            tracking_history=tracking_responses
        )
        
        return CommonResponse(
            code=200,
            message="Order tracking retrieved successfully",
            message_id="ORDER_TRACKING_RETRIEVED",
            data=tracking_detail
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error tracking order: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to track order: {str(e)}"
        )


# ============================================
# RESTAURANT OWNER APIS
# ============================================

@router.get("/restaurant/pending", response_model=CommonResponse[RestaurantOrdersResponse])
async def get_restaurant_pending_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get pending orders for restaurant (awaiting acceptance).
    
    Only accessible by restaurant owners.
    """
    try:
        # Verify user is restaurant owner
        if current_user.role != UserRole.RESTAURANT_OWNER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only restaurant owners can access this endpoint"
            )
        
        # Get restaurant for this owner
        restaurant = db.query(Restaurant).filter(
            Restaurant.owner_id == current_user.user_id
        ).first()
        
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found for this owner"
            )
        
        # Get pending orders
        query = db.query(Order).filter(
            Order.restaurant_id == restaurant.restaurant_id,
            Order.order_status == OrderStatus.PENDING
        )
        
        total_count = query.count()
        offset = (page - 1) * limit
        orders = query.order_by(Order.created_at).offset(offset).limit(limit).all()
        
        # Build response
        order_responses = []
        for order in orders:
            customer = db.query(User).filter(User.user_id == order.customer_id).first()
            order_items = db.query(OrderItem).filter(OrderItem.order_id == order.order_id).all()
            
            # Build item responses
            item_responses = []
            for item in order_items:
                food_item = db.query(FoodItem).filter(FoodItem.food_item_id == item.food_item_id).first()
                item_responses.append(OrderItemResponse(
                    order_item_id=item.order_item_id,
                    food_item_id=item.food_item_id,
                    food_item_name=food_item.name if food_item else "Unknown",
                    food_item_image=food_item.image if food_item else None,
                    variant_id=item.variant_id,
                    variant_name=None,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    total_price=item.total_price,
                    special_instructions=item.special_instructions,
                    is_veg=food_item.is_veg if food_item else True
                ))
            
            order_response = RestaurantOrderResponse(
                order_id=order.order_id,
                order_number=order.order_number,
                customer_name=f"{customer.first_name} {customer.last_name}" if customer else "Unknown",
                customer_phone=customer.phone if customer else "",
                items=item_responses,
                subtotal=order.subtotal,
                total_amount=order.total_amount,
                payment_method=order.payment_method,
                payment_status=order.payment_status,
                order_status=order.order_status,
                special_instructions=order.special_instructions,
                estimated_delivery_time=order.estimated_delivery_time,
                created_at=order.created_at
            )
            order_responses.append(order_response)
        
        has_more = (offset + limit) < total_count
        
        return CommonResponse(
            code=200,
            message=f"Found {len(order_responses)} pending orders",
            message_id="RESTAURANT_PENDING_ORDERS",
            data=RestaurantOrdersResponse(
                orders=order_responses,
                total_count=total_count,
                has_more=has_more
            )
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching pending orders: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch pending orders: {str(e)}"
        )


@router.post("/{order_id}/accept", response_model=CommonResponse[dict])
async def accept_order(
    order_id: UUID,
    request: OrderAcceptRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Accept order and set preparation time.
    
    Only accessible by restaurant owners.
    """
    try:
        # Verify user is restaurant owner
        if current_user.role != UserRole.RESTAURANT_OWNER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only restaurant owners can accept orders"
            )
        
        # Get order
        order = db.query(Order).filter(Order.order_id == order_id).first()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # Verify restaurant ownership
        restaurant = db.query(Restaurant).filter(
            Restaurant.restaurant_id == order.restaurant_id,
            Restaurant.owner_id == current_user.user_id
        ).first()
        
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to accept this order"
            )
        
        # Check order status
        if order.order_status != OrderStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Order cannot be accepted in {order.order_status.value} status"
            )
        
        # Update order
        order.order_status = OrderStatus.CONFIRMED
        order.updated_at = datetime.now(timezone.utc)
        
        # Update estimated delivery time based on prep time
        from app.utils.order_utils import calculate_estimated_delivery_time
        address = db.query(Address).filter(Address.address_id == order.delivery_address_id).first()
        distance_km = calculate_distance(
            float(address.latitude) if address.latitude else 0,
            float(address.longitude) if address.longitude else 0,
            float(restaurant.latitude),
            float(restaurant.longitude)
        )
        order.estimated_delivery_time = calculate_estimated_delivery_time(
            request.estimated_prep_time,
            distance_km
        )
        
        # Create tracking record
        tracking = OrderTracking(
            order_id=order_id,
            status=OrderStatus.CONFIRMED,
            notes=f"Order accepted. Estimated prep time: {request.estimated_prep_time} minutes"
        )
        db.add(tracking)
        
        db.commit()
        
        logger.info(f"Order {order.order_number} accepted by restaurant")
        
        # TODO: Notify customer
        
        return CommonResponse(
            code=200,
            message="Order accepted successfully",
            message_id="ORDER_ACCEPTED",
            data={"order_id": str(order_id), "estimated_prep_time": request.estimated_prep_time}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error accepting order: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to accept order: {str(e)}"
        )


@router.post("/{order_id}/reject", response_model=CommonResponse[dict])
async def reject_order(
    order_id: UUID,
    request: OrderRejectRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Reject order with reason.
    
    Only accessible by restaurant owners.
    """
    try:
        # Verify user is restaurant owner
        if current_user.role != UserRole.RESTAURANT_OWNER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only restaurant owners can reject orders"
            )
        
        # Get order
        order = db.query(Order).filter(Order.order_id == order_id).first()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # Verify restaurant ownership
        restaurant = db.query(Restaurant).filter(
            Restaurant.restaurant_id == order.restaurant_id,
            Restaurant.owner_id == current_user.user_id
        ).first()
        
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to reject this order"
            )
        
        # Check order status
        if order.order_status != OrderStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Order cannot be rejected in {order.order_status.value} status"
            )
        
        # Update order
        order.order_status = OrderStatus.CANCELLED
        order.cancellation_reason = f"Rejected by restaurant: {request.rejection_reason}"
        order.updated_at = datetime.now(timezone.utc)
        
        # Create tracking record
        tracking = OrderTracking(
            order_id=order_id,
            status=OrderStatus.CANCELLED,
            notes=order.cancellation_reason
        )
        db.add(tracking)
        
        db.commit()
        
        logger.info(f"Order {order.order_number} rejected by restaurant")
        
        # TODO: Process refund if paid
        # TODO: Notify customer
        
        return CommonResponse(
            code=200,
            message="Order rejected successfully",
            message_id="ORDER_REJECTED",
            data={"order_id": str(order_id), "reason": request.rejection_reason}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error rejecting order: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reject order: {str(e)}"
        )


@router.post("/{order_id}/update-status", response_model=CommonResponse[dict])
async def update_order_status_restaurant(
    order_id: UUID,
    request: OrderStatusUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update order status (preparing, ready_for_pickup).
    
    Only accessible by restaurant owners.
    """
    try:
        # Verify user is restaurant owner
        if current_user.role != UserRole.RESTAURANT_OWNER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only restaurant owners can update order status"
            )
        
        # Get order
        order = db.query(Order).filter(Order.order_id == order_id).first()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # Verify restaurant ownership
        restaurant = db.query(Restaurant).filter(
            Restaurant.restaurant_id == order.restaurant_id,
            Restaurant.owner_id == current_user.user_id
        ).first()
        
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to update this order"
            )
        
        # Update status using service
        updated_order = OrderService.update_order_status(
            db=db,
            order_id=order_id,
            new_status=request.status,
            notes=request.notes
        )
        
        # TODO: Notify customer and delivery partner if ready
        
        return CommonResponse(
            code=200,
            message=f"Order status updated to {request.status.value}",
            message_id="ORDER_STATUS_UPDATED",
            data={"order_id": str(order_id), "status": request.status.value}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating order status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update order status: {str(e)}"
        )


@router.get("/restaurant/active", response_model=CommonResponse[RestaurantOrdersResponse])
async def get_restaurant_active_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get active orders for restaurant (confirmed, preparing, ready_for_pickup)."""
    try:
        if current_user.role != UserRole.RESTAURANT_OWNER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only restaurant owners can access this endpoint")
        
        restaurant = db.query(Restaurant).filter(Restaurant.owner_id == current_user.user_id).first()
        if not restaurant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
        
        query = db.query(Order).filter(
            Order.restaurant_id == restaurant.restaurant_id,
            Order.order_status.in_([OrderStatus.CONFIRMED, OrderStatus.PREPARING, OrderStatus.READY_FOR_PICKUP])
        )
        
        total_count = query.count()
        offset = (page - 1) * limit
        orders = query.order_by(Order.created_at).offset(offset).limit(limit).all()
        
        order_responses = []
        for order in orders:
            customer = db.query(User).filter(User.user_id == order.customer_id).first()
            order_items = db.query(OrderItem).filter(OrderItem.order_id == order.order_id).all()
            
            item_responses = []
            for item in order_items:
                food_item = db.query(FoodItem).filter(FoodItem.food_item_id == item.food_item_id).first()
                item_responses.append(OrderItemResponse(
                    order_item_id=item.order_item_id, food_item_id=item.food_item_id,
                    food_item_name=food_item.name if food_item else "Unknown",
                    food_item_image=food_item.image if food_item else None,
                    variant_id=item.variant_id, variant_name=None, quantity=item.quantity,
                    unit_price=item.unit_price, total_price=item.total_price,
                    special_instructions=item.special_instructions,
                    is_veg=food_item.is_veg if food_item else True
                ))
            
            order_responses.append(RestaurantOrderResponse(
                order_id=order.order_id, order_number=order.order_number,
                customer_name=f"{customer.first_name} {customer.last_name}" if customer else "Unknown",
                customer_phone=customer.phone if customer else "", items=item_responses,
                subtotal=order.subtotal, total_amount=order.total_amount,
                payment_method=order.payment_method, payment_status=order.payment_status,
                order_status=order.order_status, special_instructions=order.special_instructions,
                estimated_delivery_time=order.estimated_delivery_time, created_at=order.created_at
            ))
        
        return CommonResponse(code=200, message=f"Found {len(order_responses)} active orders",
            message_id="RESTAURANT_ACTIVE_ORDERS",
            data=RestaurantOrdersResponse(orders=order_responses, total_count=total_count, has_more=(offset + limit) < total_count))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching active orders: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch active orders: {str(e)}")


@router.get("/restaurant/history", response_model=CommonResponse[RestaurantOrdersResponse])
async def get_restaurant_order_history(
    from_date: Optional[datetime] = Query(None), to_date: Optional[datetime] = Query(None),
    page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get completed/cancelled order history for restaurant."""
    try:
        if current_user.role != UserRole.RESTAURANT_OWNER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only restaurant owners can access this endpoint")
        
        restaurant = db.query(Restaurant).filter(Restaurant.owner_id == current_user.user_id).first()
        if not restaurant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
        
        query = db.query(Order).filter(
            Order.restaurant_id == restaurant.restaurant_id,
            Order.order_status.in_([OrderStatus.DELIVERED, OrderStatus.CANCELLED])
        )
        
        if from_date:
            query = query.filter(Order.created_at >= from_date)
        if to_date:
            query = query.filter(Order.created_at <= to_date)
        
        total_count = query.count()
        offset = (page - 1) * limit
        orders = query.order_by(desc(Order.created_at)).offset(offset).limit(limit).all()
        
        order_responses = []
        for order in orders:
            customer = db.query(User).filter(User.user_id == order.customer_id).first()
            order_items = db.query(OrderItem).filter(OrderItem.order_id == order.order_id).all()
            item_responses = [OrderItemResponse(
                order_item_id=item.order_item_id, food_item_id=item.food_item_id,
                food_item_name=db.query(FoodItem).filter(FoodItem.food_item_id == item.food_item_id).first().name if db.query(FoodItem).filter(FoodItem.food_item_id == item.food_item_id).first() else "Unknown",
                food_item_image=None, variant_id=item.variant_id, variant_name=None,
                quantity=item.quantity, unit_price=item.unit_price, total_price=item.total_price,
                special_instructions=item.special_instructions, is_veg=True
            ) for item in order_items]
            
            order_responses.append(RestaurantOrderResponse(
                order_id=order.order_id, order_number=order.order_number,
                customer_name=f"{customer.first_name} {customer.last_name}" if customer else "Unknown",
                customer_phone=customer.phone if customer else "", items=item_responses,
                subtotal=order.subtotal, total_amount=order.total_amount,
                payment_method=order.payment_method, payment_status=order.payment_status,
                order_status=order.order_status, special_instructions=order.special_instructions,
                estimated_delivery_time=order.estimated_delivery_time, created_at=order.created_at
            ))
        
        return CommonResponse(code=200, message=f"Found {len(order_responses)} historical orders",
            message_id="RESTAURANT_ORDER_HISTORY",
            data=RestaurantOrdersResponse(orders=order_responses, total_count=total_count, has_more=(offset + limit) < total_count))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch order history: {str(e)}")


@router.get("/restaurant/analytics", response_model=CommonResponse[RestaurantAnalyticsResponse])
async def get_restaurant_analytics(
    from_date: Optional[datetime] = Query(None), to_date: Optional[datetime] = Query(None),
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get restaurant order analytics."""
    try:
        if current_user.role != UserRole.RESTAURANT_OWNER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only restaurant owners can access this endpoint")
        
        restaurant = db.query(Restaurant).filter(Restaurant.owner_id == current_user.user_id).first()
        if not restaurant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
        
        query = db.query(Order).filter(Order.restaurant_id == restaurant.restaurant_id)
        if from_date:
            query = query.filter(Order.created_at >= from_date)
        if to_date:
            query = query.filter(Order.created_at <= to_date)
        
        total_orders = query.count()
        total_revenue = query.filter(Order.order_status == OrderStatus.DELIVERED).with_entities(func.sum(Order.total_amount)).scalar() or Decimal('0.00')
        avg_order_value = total_revenue / total_orders if total_orders > 0 else Decimal('0.00')
        pending_orders = query.filter(Order.order_status == OrderStatus.PENDING).count()
        completed_orders = query.filter(Order.order_status == OrderStatus.DELIVERED).count()
        cancelled_orders = query.filter(Order.order_status == OrderStatus.CANCELLED).count()
        
        return CommonResponse(code=200, message="Analytics retrieved successfully", message_id="RESTAURANT_ANALYTICS",
            data=RestaurantAnalyticsResponse(
                total_orders=total_orders, total_revenue=total_revenue, avg_order_value=avg_order_value,
                pending_orders=pending_orders, completed_orders=completed_orders, cancelled_orders=cancelled_orders,
                popular_items=[], revenue_by_date=[]
            ))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch analytics: {str(e)}")


# ============================================
# DELIVERY PARTNER APIS
# ============================================

@router.get("/delivery/available", response_model=CommonResponse[AvailableDeliveriesResponse])
async def get_available_deliveries(
    latitude: float = Query(..., ge=-90, le=90), longitude: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(10.0, ge=1, le=50),
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get available orders for delivery nearby."""
    try:
        if current_user.role != UserRole.DELIVERY_PARTNER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only delivery partners can access this endpoint")
        
        orders = db.query(Order).filter(Order.order_status == OrderStatus.READY_FOR_PICKUP, Order.delivery_partner_id == None).all()
        
        available_deliveries = []
        for order in orders:
            restaurant = db.query(Restaurant).filter(Restaurant.restaurant_id == order.restaurant_id).first()
            address = db.query(Address).filter(Address.address_id == order.delivery_address_id).first()
            customer = db.query(User).filter(User.user_id == order.customer_id).first()
            
            distance_km = calculate_distance(latitude, longitude, float(restaurant.latitude), float(restaurant.longitude))
            if distance_km <= radius_km:
                available_deliveries.append(DeliveryOrderResponse(
                    order_id=order.order_id, order_number=order.order_number,
                    restaurant=RestaurantBasicResponse(restaurant_id=restaurant.restaurant_id, name=restaurant.name,
                        phone=restaurant.phone, image=restaurant.image, address_line1=restaurant.address_line1, city=restaurant.city),
                    delivery_address=AddressResponse(address_id=address.address_id, title=address.title,
                        address_line1=address.address_line1, address_line2=address.address_line2,
                        city=address.city, state=address.state, postal_code=address.postal_code,
                        latitude=address.latitude, longitude=address.longitude),
                    customer_name=f"{customer.first_name} {customer.last_name}" if customer else "Unknown",
                    customer_phone=customer.phone if customer else "", total_amount=order.total_amount,
                    payment_method=order.payment_method, order_status=order.order_status,
                    estimated_delivery_time=order.estimated_delivery_time, distance_km=distance_km,
                    delivery_fee=order.delivery_fee, created_at=order.created_at
                ))
        
        return CommonResponse(code=200, message=f"Found {len(available_deliveries)} available deliveries",
            message_id="AVAILABLE_DELIVERIES", data=AvailableDeliveriesResponse(deliveries=available_deliveries, total_count=len(available_deliveries)))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch available deliveries: {str(e)}")


@router.post("/{order_id}/accept-delivery", response_model=CommonResponse[dict])
async def accept_delivery(
    order_id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Accept delivery assignment."""
    try:
        if current_user.role != UserRole.DELIVERY_PARTNER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only delivery partners can accept deliveries")
        
        order = db.query(Order).filter(Order.order_id == order_id, Order.order_status == OrderStatus.READY_FOR_PICKUP).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found or not ready for pickup")
        
        order.delivery_partner_id = current_user.user_id
        order.order_status = OrderStatus.PICKED_UP
        order.updated_at = datetime.now(timezone.utc)
        
        tracking = OrderTracking(order_id=order_id, status=OrderStatus.PICKED_UP, notes="Delivery partner assigned and order picked up")
        db.add(tracking)
        db.commit()
        
        logger.info(f"Order {order.order_number} accepted by delivery partner {current_user.user_id}")
        return CommonResponse(code=200, message="Delivery accepted successfully", message_id="DELIVERY_ACCEPTED",
            data={"order_id": str(order_id), "delivery_partner_id": str(current_user.user_id)})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to accept delivery: {str(e)}")


@router.get("/delivery/active", response_model=CommonResponse[AvailableDeliveriesResponse])
async def get_active_deliveries(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get active deliveries assigned to delivery partner."""
    try:
        if current_user.role != UserRole.DELIVERY_PARTNER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only delivery partners can access this endpoint")
        
        orders = db.query(Order).filter(
            Order.delivery_partner_id == current_user.user_id,
            Order.order_status == OrderStatus.PICKED_UP
        ).all()
        
        active_deliveries = []
        for order in orders:
            restaurant = db.query(Restaurant).filter(Restaurant.restaurant_id == order.restaurant_id).first()
            address = db.query(Address).filter(Address.address_id == order.delivery_address_id).first()
            customer = db.query(User).filter(User.user_id == order.customer_id).first()
            
            active_deliveries.append(DeliveryOrderResponse(
                order_id=order.order_id, order_number=order.order_number,
                restaurant=RestaurantBasicResponse(restaurant_id=restaurant.restaurant_id, name=restaurant.name,
                    phone=restaurant.phone, image=restaurant.image, address_line1=restaurant.address_line1, city=restaurant.city),
                delivery_address=AddressResponse(address_id=address.address_id, title=address.title,
                    address_line1=address.address_line1, address_line2=address.address_line2,
                    city=address.city, state=address.state, postal_code=address.postal_code,
                    latitude=address.latitude, longitude=address.longitude),
                customer_name=f"{customer.first_name} {customer.last_name}" if customer else "Unknown",
                customer_phone=customer.phone if customer else "", total_amount=order.total_amount,
                payment_method=order.payment_method, order_status=order.order_status,
                estimated_delivery_time=order.estimated_delivery_time, distance_km=None,
                delivery_fee=order.delivery_fee, created_at=order.created_at
            ))
        
        return CommonResponse(code=200, message=f"Found {len(active_deliveries)} active deliveries",
            message_id="ACTIVE_DELIVERIES", data=AvailableDeliveriesResponse(deliveries=active_deliveries, total_count=len(active_deliveries)))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch active deliveries: {str(e)}")


@router.post("/{order_id}/pickup-complete", response_model=CommonResponse[dict])
async def mark_pickup_complete(
    order_id: UUID, request: PickupCompleteRequest,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Mark order picked up from restaurant."""
    try:
        if current_user.role != UserRole.DELIVERY_PARTNER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only delivery partners can mark pickup complete")
        
        order = db.query(Order).filter(Order.order_id == order_id, Order.delivery_partner_id == current_user.user_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        
        tracking = OrderTracking(order_id=order_id, status=OrderStatus.PICKED_UP, notes="Order picked up from restaurant")
        db.add(tracking)
        db.commit()
        
        return CommonResponse(code=200, message="Pickup marked complete", message_id="PICKUP_COMPLETE", data={"order_id": str(order_id)})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to mark pickup complete: {str(e)}")


@router.post("/{order_id}/deliver", response_model=CommonResponse[dict])
async def mark_delivered(
    order_id: UUID, request: DeliveryCompleteRequest,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Mark order delivered to customer."""
    try:
        if current_user.role != UserRole.DELIVERY_PARTNER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only delivery partners can mark orders delivered")
        
        order = db.query(Order).filter(Order.order_id == order_id, Order.delivery_partner_id == current_user.user_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        
        order.order_status = OrderStatus.DELIVERED
        order.actual_delivery_time = datetime.now(timezone.utc)
        order.updated_at = datetime.now(timezone.utc)
        
        tracking = OrderTracking(order_id=order_id, status=OrderStatus.DELIVERED, notes="Order delivered to customer")
        db.add(tracking)
        
        # Update delivery partner stats
        delivery_partner = db.query(DeliveryPartner).filter(DeliveryPartner.user_id == current_user.user_id).first()
        if delivery_partner:
            delivery_partner.total_deliveries = (delivery_partner.total_deliveries or 0) + 1
        
        db.commit()
        
        logger.info(f"Order {order.order_number} marked as delivered")
        return CommonResponse(code=200, message="Order marked as delivered", message_id="ORDER_DELIVERED", data={"order_id": str(order_id)})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to mark order delivered: {str(e)}")


@router.post("/{order_id}/update-location", response_model=CommonResponse[dict])
async def update_delivery_location(
    order_id: UUID, request: DeliveryLocationUpdateRequest,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Update delivery partner location during delivery."""
    try:
        if current_user.role != UserRole.DELIVERY_PARTNER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only delivery partners can update location")
        
        order = db.query(Order).filter(Order.order_id == order_id, Order.delivery_partner_id == current_user.user_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        
        # Update delivery partner location
        delivery_partner = db.query(DeliveryPartner).filter(DeliveryPartner.user_id == current_user.user_id).first()
        if delivery_partner:
            delivery_partner.current_latitude = Decimal(str(request.latitude))
            delivery_partner.current_longitude = Decimal(str(request.longitude))
        
        # Create tracking record with location
        tracking = OrderTracking(
            order_id=order_id, status=order.order_status,
            latitude=Decimal(str(request.latitude)), longitude=Decimal(str(request.longitude)),
            notes="Location updated"
        )
        db.add(tracking)
        db.commit()
        
        return CommonResponse(code=200, message="Location updated", message_id="LOCATION_UPDATED",
            data={"order_id": str(order_id), "latitude": request.latitude, "longitude": request.longitude})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update location: {str(e)}")


@router.get("/delivery/earnings", response_model=CommonResponse[DeliveryEarningsResponse])
async def get_delivery_earnings(
    from_date: Optional[datetime] = Query(None), to_date: Optional[datetime] = Query(None),
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get delivery partner earnings."""
    try:
        if current_user.role != UserRole.DELIVERY_PARTNER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only delivery partners can access earnings")
        
        query = db.query(Order).filter(
            Order.delivery_partner_id == current_user.user_id,
            Order.order_status == OrderStatus.DELIVERED
        )
        if from_date:
            query = query.filter(Order.created_at >= from_date)
        if to_date:
            query = query.filter(Order.created_at <= to_date)
        
        completed_deliveries = query.count()
        total_earnings = query.with_entities(func.sum(Order.delivery_fee)).scalar() or Decimal('0.00')
        avg_per_delivery = total_earnings / completed_deliveries if completed_deliveries > 0 else Decimal('0.00')
        
        return CommonResponse(code=200, message="Earnings retrieved successfully", message_id="DELIVERY_EARNINGS",
            data=DeliveryEarningsResponse(
                total_earnings=total_earnings, completed_deliveries=completed_deliveries,
                avg_per_delivery=avg_per_delivery, earnings_by_date=[], total_distance_km=0.0
            ))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch earnings: {str(e)}")


# ============================================
# ADMIN APIS
# ============================================

@router.get("/admin/orders", response_model=CommonResponse[AdminOrdersResponse])
async def get_all_orders_admin(
    status_filter: Optional[OrderStatus] = Query(None), restaurant_id: Optional[UUID] = Query(None),
    customer_id: Optional[UUID] = Query(None), from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get all orders with filters (admin only)."""
    try:
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can access all orders")
        
        query = db.query(Order)
        if status_filter:
            query = query.filter(Order.order_status == status_filter)
        if restaurant_id:
            query = query.filter(Order.restaurant_id == restaurant_id)
        if customer_id:
            query = query.filter(Order.customer_id == customer_id)
        if from_date:
            query = query.filter(Order.created_at >= from_date)
        if to_date:
            query = query.filter(Order.created_at <= to_date)
        
        total_count = query.count()
        offset = (page - 1) * limit
        orders = query.order_by(desc(Order.created_at)).offset(offset).limit(limit).all()
        
        # Build admin order responses (simplified for now)
        order_responses = []
        for order in orders:
            customer = db.query(User).filter(User.user_id == order.customer_id).first()
            restaurant = db.query(Restaurant).filter(Restaurant.restaurant_id == order.restaurant_id).first()
            address = db.query(Address).filter(Address.address_id == order.delivery_address_id).first()
            
            order_responses.append(AdminOrderResponse(
                order_id=order.order_id, order_number=order.order_number,
                customer_id=order.customer_id, restaurant_id=order.restaurant_id,
                restaurant=RestaurantBasicResponse(restaurant_id=restaurant.restaurant_id, name=restaurant.name,
                    phone=restaurant.phone, image=restaurant.image, address_line1=restaurant.address_line1, city=restaurant.city),
                delivery_partner_id=order.delivery_partner_id, delivery_address_id=order.delivery_address_id,
                delivery_address=AddressResponse(address_id=address.address_id, title=address.title,
                    address_line1=address.address_line1, address_line2=address.address_line2,
                    city=address.city, state=address.state, postal_code=address.postal_code,
                    latitude=address.latitude, longitude=address.longitude),
                subtotal=order.subtotal, tax_amount=order.tax_amount, delivery_fee=order.delivery_fee,
                discount_amount=order.discount_amount, total_amount=order.total_amount,
                payment_method=order.payment_method, payment_status=order.payment_status, payment_id=order.payment_id,
                order_status=order.order_status, estimated_delivery_time=order.estimated_delivery_time,
                actual_delivery_time=order.actual_delivery_time, special_instructions=order.special_instructions,
                cancellation_reason=order.cancellation_reason, rating=order.rating, review=order.review,
                created_at=order.created_at, updated_at=order.updated_at, items=[], delivery_partner=None, tracking=[],
                customer_name=f"{customer.first_name} {customer.last_name}" if customer else "Unknown",
                customer_email=customer.email if customer else "", customer_phone=customer.phone if customer else ""
            ))
        
        return CommonResponse(code=200, message=f"Found {len(order_responses)} orders", message_id="ADMIN_ORDERS",
            data=AdminOrdersResponse(orders=order_responses, total_count=total_count, has_more=(offset + limit) < total_count))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch orders: {str(e)}")


@router.get("/admin/analytics", response_model=CommonResponse[AdminAnalyticsResponse])
async def get_admin_analytics(
    from_date: Optional[datetime] = Query(None), to_date: Optional[datetime] = Query(None),
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get platform-wide order analytics (admin only)."""
    try:
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can access analytics")
        
        query = db.query(Order)
        if from_date:
            query = query.filter(Order.created_at >= from_date)
        if to_date:
            query = query.filter(Order.created_at <= to_date)
        
        total_orders = query.count()
        total_revenue = query.filter(Order.order_status == OrderStatus.DELIVERED).with_entities(func.sum(Order.total_amount)).scalar() or Decimal('0.00')
        avg_order_value = total_revenue / total_orders if total_orders > 0 else Decimal('0.00')
        total_customers = db.query(User).filter(User.role == UserRole.CUSTOMER).count()
        total_restaurants = db.query(Restaurant).filter(Restaurant.status == 'active').count()
        total_delivery_partners = db.query(User).filter(User.role == UserRole.DELIVERY_PARTNER).count()
        
        orders_by_status = {
            "pending": query.filter(Order.order_status == OrderStatus.PENDING).count(),
            "confirmed": query.filter(Order.order_status == OrderStatus.CONFIRMED).count(),
            "delivered": query.filter(Order.order_status == OrderStatus.DELIVERED).count(),
            "cancelled": query.filter(Order.order_status == OrderStatus.CANCELLED).count()
        }
        
        return CommonResponse(code=200, message="Analytics retrieved successfully", message_id="ADMIN_ANALYTICS",
            data=AdminAnalyticsResponse(
                total_orders=total_orders, total_revenue=total_revenue, avg_order_value=avg_order_value,
                total_customers=total_customers, total_restaurants=total_restaurants,
                total_delivery_partners=total_delivery_partners, orders_by_status=orders_by_status,
                revenue_by_date=[], top_restaurants=[], top_customers=[]
            ))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch analytics: {str(e)}")


@router.post("/admin/{order_id}/intervene", response_model=CommonResponse[dict])
async def admin_intervene_order(
    order_id: UUID, request: AdminInterventionRequest,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Admin intervention on order (cancel, reassign delivery partner, refund)."""
    try:
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can intervene in orders")
        
        order = db.query(Order).filter(Order.order_id == order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        
        if request.action == "cancel":
            order.order_status = OrderStatus.CANCELLED
            order.cancellation_reason = f"Admin intervention: {request.reason}"
            tracking = OrderTracking(order_id=order_id, status=OrderStatus.CANCELLED, notes=order.cancellation_reason)
            db.add(tracking)
        elif request.action == "reassign_delivery":
            if not request.new_delivery_partner_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New delivery partner ID required")
            order.delivery_partner_id = request.new_delivery_partner_id
            tracking = OrderTracking(order_id=order_id, status=order.order_status, notes=f"Delivery partner reassigned: {request.reason}")
            db.add(tracking)
        elif request.action == "refund":
            order.payment_status = PaymentStatus.REFUNDED
            tracking = OrderTracking(order_id=order_id, status=order.order_status, notes=f"Refund processed: {request.reason}")
            db.add(tracking)
        
        order.updated_at = datetime.now(timezone.utc)
        db.commit()
        
        logger.info(f"Admin intervention on order {order.order_number}: {request.action}")
        return CommonResponse(code=200, message=f"Admin intervention completed: {request.action}",
            message_id="ADMIN_INTERVENTION", data={"order_id": str(order_id), "action": request.action})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to process intervention: {str(e)}")
