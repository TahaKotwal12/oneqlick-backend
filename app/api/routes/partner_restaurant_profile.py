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
# RESTAURANT PROFILE MANAGEMENT ENDPOINTS
# ============================================================================

@router.get("/profile", response_model=CommonResponse[RestaurantProfileResponse])
async def get_restaurant_profile(
    current_user: User = Depends(require_restaurant_owner),
    db: Session = Depends(get_db)
):
    """
    Get the restaurant profile for the authenticated owner.
    """
    try:
        logger.info(f"Fetching restaurant profile for owner: {current_user.user_id}")
        
        # Get restaurant owned by this user
        restaurant = db.query(Restaurant).filter(
            Restaurant.owner_id == current_user.user_id
        ).first()
        
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No restaurant found for this user"
            )
        
        # Build response
        profile_response = RestaurantProfileResponse(
            restaurant_id=restaurant.restaurant_id,
            name=restaurant.name,
            description=restaurant.description,
            phone=restaurant.phone,
            email=restaurant.email,
            address_line1=restaurant.address_line1,
            address_line2=restaurant.address_line2,
            city=restaurant.city,
            state=restaurant.state,
            postal_code=restaurant.postal_code,
            latitude=restaurant.latitude,
            longitude=restaurant.longitude,
            image=restaurant.image,
            cover_image=restaurant.cover_image,
            cuisine_type=restaurant.cuisine_type,
            avg_delivery_time=restaurant.avg_delivery_time,
            min_order_amount=restaurant.min_order_amount,
            delivery_fee=restaurant.delivery_fee,
            rating=restaurant.rating,
            total_ratings=restaurant.total_ratings,
            status=restaurant.status,
            is_open=restaurant.is_open,
            opening_time=restaurant.opening_time.strftime("%H:%M:%S") if restaurant.opening_time else None,
            closing_time=restaurant.closing_time.strftime("%H:%M:%S") if restaurant.closing_time else None,
            created_at=restaurant.created_at,
            updated_at=restaurant.updated_at
        )
        
        return CommonResponse(
            code=200,
            message="Restaurant profile retrieved successfully",
            message_id="PROFILE_RETRIEVED",
            data=profile_response
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching restaurant profile: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch restaurant profile: {str(e)}"
        )


@router.put("/profile", response_model=CommonResponse[RestaurantProfileResponse])
async def update_restaurant_profile(
    request: UpdateRestaurantProfileRequest,
    current_user: User = Depends(require_restaurant_owner),
    db: Session = Depends(get_db)
):
    """
    Update the restaurant profile.
    """
    try:
        logger.info(f"Updating restaurant profile for owner: {current_user.user_id}")
        
        # Get restaurant owned by this user
        restaurant = db.query(Restaurant).filter(
            Restaurant.owner_id == current_user.user_id
        ).first()
        
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No restaurant found for this user"
            )
        
        # Update fields if provided
        update_data = request.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            if hasattr(restaurant, field) and value is not None:
                setattr(restaurant, field, value)
        
        restaurant.updated_at = datetime.now(timezone.utc)
        
        db.commit()
        db.refresh(restaurant)
        
        logger.info(f"Restaurant profile updated: {restaurant.restaurant_id}")
        
        # Return updated profile
        return await get_restaurant_profile(current_user, db)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating restaurant profile: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update restaurant profile: {str(e)}"
        )


@router.put("/profile/operating-hours", response_model=CommonResponse[RestaurantProfileResponse])
async def update_operating_hours(
    request: UpdateOperatingHoursRequest,
    current_user: User = Depends(require_restaurant_owner),
    db: Session = Depends(get_db)
):
    """
    Update restaurant operating hours.
    """
    try:
        logger.info(f"Updating operating hours for owner: {current_user.user_id}")
        
        # Get restaurant owned by this user
        restaurant = db.query(Restaurant).filter(
            Restaurant.owner_id == current_user.user_id
        ).first()
        
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No restaurant found for this user"
            )
        
        # Update operating hours
        from datetime import time
        
        if request.opening_time:
            # Parse time string (HH:MM:SS or HH:MM)
            time_parts = request.opening_time.split(':')
            restaurant.opening_time = time(
                hour=int(time_parts[0]),
                minute=int(time_parts[1]),
                second=int(time_parts[2]) if len(time_parts) > 2 else 0
            )
        
        if request.closing_time:
            time_parts = request.closing_time.split(':')
            restaurant.closing_time = time(
                hour=int(time_parts[0]),
                minute=int(time_parts[1]),
                second=int(time_parts[2]) if len(time_parts) > 2 else 0
            )
        
        if request.is_open is not None:
            restaurant.is_open = request.is_open
        
        restaurant.updated_at = datetime.now(timezone.utc)
        
        db.commit()
        db.refresh(restaurant)
        
        logger.info(f"Operating hours updated for restaurant: {restaurant.restaurant_id}")
        
        # Return updated profile
        return await get_restaurant_profile(current_user, db)
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid time format: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error updating operating hours: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update operating hours: {str(e)}"
        )


# ============================================================================
# ORDER MANAGEMENT ENDPOINTS
# ============================================================================

# ... (rest of the existing code for orders and stats)
