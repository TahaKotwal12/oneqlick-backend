from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from typing import Optional
from datetime import datetime, timezone, timedelta
from decimal import Decimal
import logging

from app.infra.db.postgres.postgres_config import get_db
from app.api.dependencies import get_current_user, require_restaurant_owner
from app.api.schemas.partner_restaurant_schemas import (
    RestaurantOrderResponse, OrderListResponse, UpdateOrderStatusRequest,
    AddOrderNoteRequest, OrderNoteResponse, RestaurantStatsResponse,
    MenuItemResponse, MenuListResponse, CreateMenuItemRequest,
    UpdateMenuItemRequest, UpdateItemAvailabilityRequest,
    BulkUpdateMenuRequest, BulkUpdateMenuResponse,
    RestaurantProfileResponse, UpdateRestaurantProfileRequest,
    UpdateOperatingHoursRequest, CategoryResponse, CategoryListResponse,
    OrderItemResponse, DeliveryAddressResponse
)
from app.api.schemas.common_schemas import CommonResponse
from app.infra.db.postgres.models.user import User
from app.infra.db.postgres.models.order import Order
from app.infra.db.postgres.models.order_item import OrderItem
from app.infra.db.postgres.models.food_item import FoodItem
from app.infra.db.postgres.models.restaurant import Restaurant
from app.infra.db.postgres.models.category import Category
from app.infra.db.postgres.models.address import Address
from app.utils.enums import OrderStatus
from app.config.logger import get_logger

router = APIRouter(prefix="/partner/restaurant", tags=["Partner - Restaurant"])
logger = get_logger(__name__)


# ============================================================================
# ORDER MANAGEMENT ENDPOINTS
# ============================================================================

@router.get("/orders", response_model=CommonResponse[OrderListResponse])
async def get_restaurant_orders(
    status: Optional[str] = Query(None, description="Filter by order status"),
    limit: int = Query(50, ge=1, le=100, description="Number of orders to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    current_user: User = Depends(require_restaurant_owner),
    db: Session = Depends(get_db)
):
    """
    Get all orders for the restaurant owner.
    
    This endpoint returns orders for the restaurant owned by the authenticated user.
    Orders can be filtered by status and are paginated.
    """
    try:
        logger.info(f"Fetching orders for restaurant owner: {current_user.user_id}")
        
        # Get restaurant owned by this user
        restaurant = db.query(Restaurant).filter(
            Restaurant.owner_id == current_user.user_id
        ).first()
        
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No restaurant found for this user"
            )
        
        # Build query
        query = db.query(Order).filter(
            Order.restaurant_id == restaurant.restaurant_id
        )
        
        # Apply status filter if provided
        if status:
            query = query.filter(Order.order_status == status)
        
        # Get total count
        total_count = query.count()
        
        # Apply pagination and ordering
        orders = query.order_by(desc(Order.created_at)).offset(offset).limit(limit).all()
        
        # Build response
        order_responses = []
        for order in orders:
            # Get customer details
            customer = db.query(User).filter(User.user_id == order.customer_id).first()
            
            # Get order items
            order_items = db.query(OrderItem).filter(
                OrderItem.order_id == order.order_id
            ).all()
            
            items_response = []
            for item in order_items:
                # Get food item details
                food_item = db.query(FoodItem).filter(
                    FoodItem.food_item_id == item.food_item_id
                ).first()
                
                items_response.append(OrderItemResponse(
                    food_item_id=item.food_item_id,
                    name=food_item.name if food_item else "Unknown Item",
                    quantity=item.quantity,
                    price=item.price,
                    customizations=[],  # TODO: Add customizations from order_item_customizations
                    addons=[]  # TODO: Add addons from order_item_addons
                ))
            
            # Get delivery address
            delivery_address = None
            if order.delivery_address_id:
                address = db.query(Address).filter(
                    Address.address_id == order.delivery_address_id
                ).first()
                
                if address:
                    delivery_address = DeliveryAddressResponse(
                        address_line1=address.address_line1,
                        address_line2=address.address_line2,
                        city=address.city,
                        state=address.state,
                        postal_code=address.postal_code,
                        latitude=address.latitude,
                        longitude=address.longitude
                    )
            
            order_responses.append(RestaurantOrderResponse(
                order_id=order.order_id,
                order_number=order.order_number,
                customer_name=f"{customer.first_name} {customer.last_name}" if customer else "Unknown",
                customer_phone=customer.phone if customer else "N/A",
                total_amount=order.total_amount,
                subtotal=order.subtotal,
                tax_amount=order.tax_amount,
                delivery_fee=order.delivery_fee,
                discount_amount=order.discount_amount,
                order_status=order.order_status.value if hasattr(order.order_status, 'value') else str(order.order_status),
                payment_status=order.payment_status.value if hasattr(order.payment_status, 'value') else str(order.payment_status),
                payment_method=order.payment_method.value if hasattr(order.payment_method, 'value') else str(order.payment_method),
                created_at=order.created_at,
                estimated_delivery_time=order.estimated_delivery_time,
                special_instructions=order.special_instructions,
                items=items_response,
                delivery_address=delivery_address
            ))
        
        has_more = (offset + limit) < total_count
        
        logger.info(f"Found {total_count} orders, returning {len(order_responses)}")
        
        return CommonResponse(
            code=200,
            message="Orders retrieved successfully",
            message_id="ORDERS_RETRIEVED",
            data=OrderListResponse(
                orders=order_responses,
                total_count=total_count,
                has_more=has_more
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching orders: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch orders: {str(e)}"
        )


@router.get("/orders/{order_id}", response_model=CommonResponse[RestaurantOrderResponse])
async def get_order_details(
    order_id: str,
    current_user: User = Depends(require_restaurant_owner),
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific order.
    """
    try:
        # Get restaurant owned by this user
        restaurant = db.query(Restaurant).filter(
            Restaurant.owner_id == current_user.user_id
        ).first()
        
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No restaurant found for this user"
            )
        
        # Get order
        order = db.query(Order).filter(
            and_(
                Order.order_id == order_id,
                Order.restaurant_id == restaurant.restaurant_id
            )
        ).first()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # Get customer details
        customer = db.query(User).filter(User.user_id == order.customer_id).first()
        
        # Get order items
        order_items = db.query(OrderItem).filter(
            OrderItem.order_id == order.order_id
        ).all()
        
        items_response = []
        for item in order_items:
            food_item = db.query(FoodItem).filter(
                FoodItem.food_item_id == item.food_item_id
            ).first()
            
            items_response.append(OrderItemResponse(
                food_item_id=item.food_item_id,
                name=food_item.name if food_item else "Unknown Item",
                quantity=item.quantity,
                price=item.price,
                customizations=[],
                addons=[]
            ))
        
        # Get delivery address
        delivery_address = None
        if order.delivery_address_id:
            address = db.query(Address).filter(
                Address.address_id == order.delivery_address_id
            ).first()
            
            if address:
                delivery_address = DeliveryAddressResponse(
                    address_line1=address.address_line1,
                    address_line2=address.address_line2,
                    city=address.city,
                    state=address.state,
                    postal_code=address.postal_code,
                    latitude=address.latitude,
                    longitude=address.longitude
                )
        
        order_response = RestaurantOrderResponse(
            order_id=order.order_id,
            order_number=order.order_number,
            customer_name=f"{customer.first_name} {customer.last_name}" if customer else "Unknown",
            customer_phone=customer.phone if customer else "N/A",
            total_amount=order.total_amount,
            subtotal=order.subtotal,
            tax_amount=order.tax_amount,
            delivery_fee=order.delivery_fee,
            discount_amount=order.discount_amount,
            order_status=order.order_status.value if hasattr(order.order_status, 'value') else str(order.order_status),
            payment_status=order.payment_status.value if hasattr(order.payment_status, 'value') else str(order.payment_status),
            payment_method=order.payment_method.value if hasattr(order.payment_method, 'value') else str(order.payment_method),
            created_at=order.created_at,
            estimated_delivery_time=order.estimated_delivery_time,
            special_instructions=order.special_instructions,
            items=items_response,
            delivery_address=delivery_address
        )
        
        return CommonResponse(
            code=200,
            message="Order details retrieved successfully",
            message_id="ORDER_DETAILS_SUCCESS",
            data=order_response
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching order details: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch order details: {str(e)}"
        )


@router.put("/orders/{order_id}/status", response_model=CommonResponse[RestaurantOrderResponse])
async def update_order_status(
    order_id: str,
    request: UpdateOrderStatusRequest,
    current_user: User = Depends(require_restaurant_owner),
    db: Session = Depends(get_db)
):
    """
    Update the status of an order.
    
    Allowed status transitions:
    - pending -> preparing (accept order)
    - preparing -> ready_for_pickup (mark as ready)
    - pending -> rejected (reject order)
    """
    try:
        # Get restaurant owned by this user
        restaurant = db.query(Restaurant).filter(
            Restaurant.owner_id == current_user.user_id
        ).first()
        
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No restaurant found for this user"
            )
        
        # Get order
        order = db.query(Order).filter(
            and_(
                Order.order_id == order_id,
                Order.restaurant_id == restaurant.restaurant_id
            )
        ).first()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # Validate status transition
        current_status = order.order_status.value if hasattr(order.order_status, 'value') else str(order.order_status)
        new_status = request.status
        
        valid_transitions = {
            'pending': ['preparing', 'rejected'],
            'preparing': ['ready_for_pickup'],
        }
        
        if current_status not in valid_transitions or new_status not in valid_transitions[current_status]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status transition from {current_status} to {new_status}"
            )
        
        # Update order status
        order.order_status = new_status
        order.updated_at = datetime.now(timezone.utc)
        
        db.commit()
        db.refresh(order)
        
        logger.info(f"Order {order_id} status updated to {new_status}")
        
        # Return updated order (reuse get_order_details logic)
        return await get_order_details(order_id, current_user, db)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating order status: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update order status: {str(e)}"
        )


@router.get("/stats", response_model=CommonResponse[RestaurantStatsResponse])
async def get_restaurant_stats(
    current_user: User = Depends(require_restaurant_owner),
    db: Session = Depends(get_db)
):
    """
    Get restaurant statistics including today's orders, revenue, and monthly totals.
    """
    try:
        # Get restaurant owned by this user
        restaurant = db.query(Restaurant).filter(
            Restaurant.owner_id == current_user.user_id
        ).first()
        
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No restaurant found for this user"
            )
        
        # Get today's date range
        today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        
        # Get this month's date range
        month_start = datetime.now(timezone.utc).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Today's orders
        today_orders = db.query(func.count(Order.order_id)).filter(
            and_(
                Order.restaurant_id == restaurant.restaurant_id,
                Order.created_at >= today_start,
                Order.created_at < today_end
            )
        ).scalar() or 0
        
        # Pending orders
        pending_orders = db.query(func.count(Order.order_id)).filter(
            and_(
                Order.restaurant_id == restaurant.restaurant_id,
                Order.order_status == 'pending'
            )
        ).scalar() or 0
        
        # Today's revenue
        revenue_today = db.query(func.sum(Order.total_amount)).filter(
            and_(
                Order.restaurant_id == restaurant.restaurant_id,
                Order.created_at >= today_start,
                Order.created_at < today_end,
                Order.payment_status == 'paid'
            )
        ).scalar() or Decimal('0.00')
        
        # This month's orders
        total_orders_this_month = db.query(func.count(Order.order_id)).filter(
            and_(
                Order.restaurant_id == restaurant.restaurant_id,
                Order.created_at >= month_start
            )
        ).scalar() or 0
        
        # This month's revenue
        revenue_this_month = db.query(func.sum(Order.total_amount)).filter(
            and_(
                Order.restaurant_id == restaurant.restaurant_id,
                Order.created_at >= month_start,
                Order.payment_status == 'paid'
            )
        ).scalar() or Decimal('0.00')
        
        # Average preparation time (placeholder - would need order_status_history table)
        avg_preparation_time = 25  # Default value
        
        return CommonResponse(
            code=200,
            message="Statistics retrieved successfully",
            message_id="STATS_SUCCESS",
            data=RestaurantStatsResponse(
                today_orders=today_orders,
                pending_orders=pending_orders,
                revenue_today=revenue_today,
                avg_preparation_time=avg_preparation_time,
                total_orders_this_month=total_orders_this_month,
                revenue_this_month=revenue_this_month
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching restaurant stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch statistics: {str(e)}"
        )
