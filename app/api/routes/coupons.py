from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import Optional, List
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from app.infra.db.postgres.postgres_config import get_db
from app.api.dependencies import get_current_user, get_optional_current_user
from app.infra.db.postgres.models.user import User
from app.infra.db.postgres.models.coupon import Coupon
from app.infra.db.postgres.models.user_coupon_usage import UserCouponUsage
from app.infra.db.postgres.models.restaurant_offer import RestaurantOffer
from app.infra.db.postgres.models.order import Order
from app.api.schemas.coupon_schemas import (
    CouponResponse,
    CouponListResponse,
    ValidateCouponRequest,
    ValidateCouponResponse,
    ApplyCouponRequest,
    ApplyCouponResponse,
    RestaurantOfferResponse,
    OffersListResponse,
    CouponUsageResponse,
    CouponUsageListResponse,
    CarouselCouponResponse,
    CarouselCouponsListResponse
)
from app.utils.enums import CouponType
from app.config.logger import get_logger

router = APIRouter(prefix="/coupons", tags=["coupons"])
logger = get_logger(__name__)


def calculate_discount(
    coupon: Coupon,
    cart_total: Decimal
) -> Decimal:
    """
    Calculate discount amount based on coupon type and cart total.
    
    Args:
        coupon: Coupon object
        cart_total: Cart subtotal amount
        
    Returns:
        Calculated discount amount
    """
    discount_amount = Decimal('0.00')
    
    if coupon.coupon_type == CouponType.PERCENTAGE:
        # Calculate percentage discount
        discount_amount = (cart_total * coupon.discount_value) / Decimal('100')
        
        # Apply max discount cap if specified
        if coupon.max_discount_amount:
            discount_amount = min(discount_amount, coupon.max_discount_amount)
            
    elif coupon.coupon_type == CouponType.FIXED_AMOUNT:
        # Fixed amount discount
        discount_amount = coupon.discount_value
        
    elif coupon.coupon_type == CouponType.FREE_DELIVERY:
        # Free delivery - discount will be applied to delivery fee
        # For now, return 0 as delivery fee is handled separately
        discount_amount = Decimal('0.00')
    
    # Ensure discount doesn't exceed cart total
    discount_amount = min(discount_amount, cart_total)
    
    return discount_amount


def is_coupon_valid(
    coupon: Coupon,
    cart_total: Decimal,
    user_id: Optional[UUID],
    db: Session
) -> tuple[bool, Optional[str]]:
    """
    Validate if coupon can be used.
    
    Args:
        coupon: Coupon object
        cart_total: Cart subtotal amount
        user_id: User ID (optional for guest users)
        db: Database session
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    now = datetime.now(timezone.utc)
    
    # Check if coupon is active
    if not coupon.is_active:
        return False, "This coupon is no longer active"
    
    # Check if coupon has expired
    if coupon.valid_until < now:
        return False, "This coupon has expired"
    
    # Check if coupon is not yet valid
    if coupon.valid_from > now:
        return False, "This coupon is not yet valid"
    
    # Check minimum order amount
    if cart_total < coupon.min_order_amount:
        return False, f"Minimum order amount of ₹{coupon.min_order_amount} required"
    
    # Check usage limit
    if coupon.usage_limit and coupon.used_count >= coupon.usage_limit:
        return False, "This coupon has reached its usage limit"
    
    # Check if user has already used this coupon (if user is logged in)
    if user_id:
        user_usage_count = db.query(func.count(UserCouponUsage.user_coupon_usage_id))\
            .filter(
                UserCouponUsage.user_id == user_id,
                UserCouponUsage.coupon_id == coupon.coupon_id
            ).scalar()
        
        # For now, allow one use per user (can be made configurable)
        if user_usage_count > 0:
            return False, "You have already used this coupon"
    
    return True, None


@router.get("", response_model=CouponListResponse)
async def get_available_coupons(
    restaurant_id: Optional[UUID] = Query(None, description="Filter by restaurant ID"),
    min_order_amount: Optional[Decimal] = Query(None, description="Filter by minimum order amount"),
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all available coupons.
    
    Returns list of active, non-expired coupons that the user can use.
    Optionally filter by restaurant and minimum order amount.
    
    **Authentication:** Optional (returns all coupons for guests, personalized for logged-in users)
    
    **Headers:**
    - `Authorization: Bearer {access_token}` (optional)
    """
    logger.info(f"Fetching available coupons for user: {current_user.user_id if current_user else 'guest'}")
    
    now = datetime.now(timezone.utc)
    
    # Base query for active, non-expired coupons
    query = db.query(Coupon).filter(
        Coupon.is_active == True,
        Coupon.valid_from <= now,
        Coupon.valid_until >= now
    )
    
    # Filter by minimum order amount if provided
    if min_order_amount:
        query = query.filter(Coupon.min_order_amount <= min_order_amount)
    
    # Get all matching coupons
    coupons = query.order_by(Coupon.discount_value.desc()).all()
    
    # Process coupons and add computed fields
    coupon_responses = []
    available_count = 0
    
    for coupon in coupons:
        # Check if coupon is still available
        is_available = True
        
        # Check usage limit
        if coupon.usage_limit and coupon.used_count >= coupon.usage_limit:
            is_available = False
        
        # Check if user has already used this coupon
        if current_user and is_available:
            user_usage_count = db.query(func.count(UserCouponUsage.user_coupon_usage_id))\
                .filter(
                    UserCouponUsage.user_id == current_user.user_id,
                    UserCouponUsage.coupon_id == coupon.coupon_id
                ).scalar()
            
            if user_usage_count > 0:
                is_available = False
        
        # Calculate usage remaining
        usage_remaining = None
        if coupon.usage_limit:
            usage_remaining = coupon.usage_limit - coupon.used_count
        
        if is_available:
            available_count += 1
        
        coupon_response = CouponResponse(
            coupon_id=coupon.coupon_id,
            code=coupon.code,
            title=coupon.title,
            description=coupon.description,
            coupon_type=coupon.coupon_type,
            discount_value=coupon.discount_value,
            min_order_amount=coupon.min_order_amount,
            max_discount_amount=coupon.max_discount_amount,
            usage_limit=coupon.usage_limit,
            used_count=coupon.used_count,
            valid_from=coupon.valid_from,
            valid_until=coupon.valid_until,
            is_active=coupon.is_active,
            created_at=coupon.created_at,
            is_expired=False,
            is_available=is_available,
            usage_remaining=usage_remaining
        )
        coupon_responses.append(coupon_response)
    
    logger.info(f"Found {len(coupon_responses)} coupons, {available_count} available")
    
    return CouponListResponse(
        coupons=coupon_responses,
        total_count=len(coupon_responses),
        available_count=available_count
    )


@router.post("/validate", response_model=ValidateCouponResponse)
async def validate_coupon(
    request: ValidateCouponRequest,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Validate a coupon code.
    
    Checks if the coupon is valid for the given cart total and returns
    the calculated discount amount.
    
    **Authentication:** Optional (works for both guests and logged-in users)
    
    **Headers:**
    - `Authorization: Bearer {access_token}` (optional)
    
    **Request Body:**
    ```json
    {
        "coupon_code": "SAVE20",
        "cart_total": 360.00,
        "restaurant_id": "uuid" (optional)
    }
    ```
    
    **Response:**
    ```json
    {
        "is_valid": true,
        "coupon": {...},
        "discount_amount": 72.00,
        "final_amount": 288.00,
        "error_message": null
    }
    ```
    """
    logger.info(f"Validating coupon: {request.coupon_code} for amount: {request.cart_total}")
    
    # Find coupon by code (case-insensitive)
    coupon = db.query(Coupon).filter(
        func.upper(Coupon.code) == request.coupon_code.upper()
    ).first()
    
    if not coupon:
        logger.warning(f"Coupon not found: {request.coupon_code}")
        return ValidateCouponResponse(
            is_valid=False,
            final_amount=request.cart_total,
            error_message="Invalid coupon code"
        )
    
    # Validate coupon
    user_id = current_user.user_id if current_user else None
    is_valid, error_message = is_coupon_valid(coupon, request.cart_total, user_id, db)
    
    if not is_valid:
        logger.warning(f"Coupon validation failed: {error_message}")
        return ValidateCouponResponse(
            is_valid=False,
            final_amount=request.cart_total,
            error_message=error_message
        )
    
    # Calculate discount
    discount_amount = calculate_discount(coupon, request.cart_total)
    final_amount = request.cart_total - discount_amount
    
    # Prepare coupon response
    coupon_response = CouponResponse(
        coupon_id=coupon.coupon_id,
        code=coupon.code,
        title=coupon.title,
        description=coupon.description,
        coupon_type=coupon.coupon_type,
        discount_value=coupon.discount_value,
        min_order_amount=coupon.min_order_amount,
        max_discount_amount=coupon.max_discount_amount,
        usage_limit=coupon.usage_limit,
        used_count=coupon.used_count,
        valid_from=coupon.valid_from,
        valid_until=coupon.valid_until,
        is_active=coupon.is_active,
        created_at=coupon.created_at,
        is_expired=False,
        is_available=True,
        usage_remaining=coupon.usage_limit - coupon.used_count if coupon.usage_limit else None
    )
    
    logger.info(f"Coupon valid. Discount: {discount_amount}, Final: {final_amount}")
    
    return ValidateCouponResponse(
        is_valid=True,
        coupon=coupon_response,
        discount_amount=discount_amount,
        final_amount=final_amount,
        error_message=None
    )


@router.get("/my-usage", response_model=CouponUsageListResponse)
async def get_my_coupon_usage(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's coupon usage history.
    
    Returns a list of all coupons used by the user with order details
    and total savings.
    
    **Authentication:** Required
    
    **Headers:**
    - `Authorization: Bearer {access_token}` (required)
    """
    logger.info(f"Fetching coupon usage history for user: {current_user.user_id}")
    
    # Calculate offset
    offset = (page - 1) * page_size
    
    # Query user's coupon usage with joins
    query = db.query(
        UserCouponUsage,
        Coupon,
        Order
    ).join(
        Coupon, UserCouponUsage.coupon_id == Coupon.coupon_id
    ).join(
        Order, UserCouponUsage.order_id == Order.order_id
    ).filter(
        UserCouponUsage.user_id == current_user.user_id
    ).order_by(
        UserCouponUsage.used_at.desc()
    )
    
    # Get total count
    total_count = query.count()
    
    # Get paginated results
    usage_records = query.offset(offset).limit(page_size).all()
    
    # Calculate total savings
    total_savings = db.query(func.sum(Order.discount_amount))\
        .join(UserCouponUsage, Order.order_id == UserCouponUsage.order_id)\
        .filter(UserCouponUsage.user_id == current_user.user_id)\
        .scalar() or Decimal('0.00')
    
    # Prepare response
    usage_history = []
    for usage, coupon, order in usage_records:
        usage_response = CouponUsageResponse(
            user_coupon_usage_id=usage.user_coupon_usage_id,
            coupon_code=coupon.code,
            coupon_title=coupon.title,
            order_id=order.order_id,
            order_number=order.order_number,
            discount_amount=order.discount_amount,
            used_at=usage.used_at
        )
        usage_history.append(usage_response)
    
    logger.info(f"Found {total_count} coupon usage records, total savings: {total_savings}")
    
    return CouponUsageListResponse(
        usage_history=usage_history,
        total_count=total_count,
        total_savings=total_savings
    )


@router.get("/offers", response_model=OffersListResponse)
async def get_active_offers(
    restaurant_id: Optional[UUID] = Query(None, description="Filter by restaurant ID"),
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all active restaurant offers.
    
    Returns list of active, non-expired restaurant-specific offers.
    Optionally filter by restaurant ID.
    
    **Authentication:** Optional
    
    **Headers:**
    - `Authorization: Bearer {access_token}` (optional)
    """
    logger.info(f"Fetching active offers for restaurant: {restaurant_id or 'all'}")
    
    now = datetime.now(timezone.utc)
    
    # Base query for active, non-expired offers
    query = db.query(RestaurantOffer).filter(
        RestaurantOffer.is_active == True,
        RestaurantOffer.valid_from <= now,
        RestaurantOffer.valid_until >= now
    )
    
    # Filter by restaurant if provided
    if restaurant_id:
        query = query.filter(RestaurantOffer.restaurant_id == restaurant_id)
    
    # Get all matching offers
    offers = query.order_by(RestaurantOffer.created_at.desc()).all()
    
    # Process offers and add computed fields
    offer_responses = []
    for offer in offers:
        offer_response = RestaurantOfferResponse(
            offer_id=offer.offer_id,
            restaurant_id=offer.restaurant_id,
            title=offer.title,
            description=offer.description,
            discount_type=offer.discount_type,
            discount_value=offer.discount_value,
            min_order_amount=offer.min_order_amount,
            max_discount_amount=offer.max_discount_amount,
            valid_from=offer.valid_from,
            valid_until=offer.valid_until,
            is_active=offer.is_active,
            created_at=offer.created_at,
            is_expired=False
        )
        offer_responses.append(offer_response)
    
    logger.info(f"Found {len(offer_responses)} active offers")
    
    return OffersListResponse(
        offers=offer_responses,
        total_count=len(offer_responses)
    )


@router.get("/restaurants/{restaurant_id}/offers", response_model=OffersListResponse)
async def get_restaurant_offers(
    restaurant_id: UUID,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all active offers for a specific restaurant.
    
    **Authentication:** Optional
    
    **Headers:**
    - `Authorization: Bearer {access_token}` (optional)
    """
    logger.info(f"Fetching offers for restaurant: {restaurant_id}")
    
    now = datetime.now(timezone.utc)
    
    # Query active offers for the restaurant
    offers = db.query(RestaurantOffer).filter(
        RestaurantOffer.restaurant_id == restaurant_id,
        RestaurantOffer.is_active == True,
        RestaurantOffer.valid_from <= now,
        RestaurantOffer.valid_until >= now
    ).order_by(RestaurantOffer.created_at.desc()).all()
    
    # Process offers
    offer_responses = []
    for offer in offers:
        offer_response = RestaurantOfferResponse(
            offer_id=offer.offer_id,
            restaurant_id=offer.restaurant_id,
            title=offer.title,
            description=offer.description,
            discount_type=offer.discount_type,
            discount_value=offer.discount_value,
            min_order_amount=offer.min_order_amount,
            max_discount_amount=offer.max_discount_amount,
            valid_from=offer.valid_from,
            valid_until=offer.valid_until,
            is_active=offer.is_active,
            created_at=offer.created_at,
            is_expired=False
        )
        offer_responses.append(offer_response)
    
    logger.info(f"Found {len(offer_responses)} offers for restaurant")
    
    return OffersListResponse(
        offers=offer_responses,
        total_count=len(offer_responses)
    )


@router.get("/carousel", response_model=CarouselCouponsListResponse)
async def get_carousel_coupons(
    db: Session = Depends(get_db)
):
    """
    Get coupons configured for carousel display on home screen.
    
    Returns coupons where show_in_carousel is True, sorted by carousel_priority.
    Includes all carousel-specific fields like gradients, icons, badges, etc.
    
    **Authentication:** Not required (public endpoint)
    """
    logger.info("Fetching carousel coupons")
    
    now = datetime.now(timezone.utc)
    
    # Query coupons marked for carousel display
    coupons = db.query(Coupon).filter(
        Coupon.is_active == True,
        Coupon.show_in_carousel == True,
        Coupon.valid_from <= now,
        Coupon.valid_until >= now
    ).order_by(Coupon.carousel_priority.desc()).all()
    
    # Process coupons and add computed fields
    carousel_responses = []
    
    for coupon in coupons:
        # Check if expired
        is_expired = coupon.valid_until < now
        
        # Format discount display
        discount_display = ""
        if coupon.coupon_type == CouponType.PERCENTAGE:
            discount_display = f"{int(coupon.discount_value)}%"
        elif coupon.coupon_type == CouponType.FIXED_AMOUNT:
            discount_display = f"₹{int(coupon.discount_value)}"
        elif coupon.coupon_type == CouponType.FREE_DELIVERY:
            discount_display = "FREE"
        
        carousel_response = CarouselCouponResponse(
            coupon_id=coupon.coupon_id,
            code=coupon.code,
            title=coupon.title,
            description=coupon.description,
            coupon_type=coupon.coupon_type,
            discount_value=coupon.discount_value,
            min_order_amount=coupon.min_order_amount,
            max_discount_amount=coupon.max_discount_amount,
            carousel_title=coupon.carousel_title or coupon.title,
            carousel_subtitle=coupon.carousel_subtitle or f"Save {discount_display}",
            carousel_badge=coupon.carousel_badge,
            carousel_icon=coupon.carousel_icon or "percent",
            carousel_gradient_start=coupon.carousel_gradient_start,
            carousel_gradient_middle=coupon.carousel_gradient_middle,
            carousel_gradient_end=coupon.carousel_gradient_end,
            carousel_action_text=coupon.carousel_action_text,
            carousel_priority=coupon.carousel_priority,
            is_expired=is_expired,
            discount_display=discount_display
        )
        
        carousel_responses.append(carousel_response)
    
    logger.info(f"Found {len(carousel_responses)} carousel coupons")
    
    return CarouselCouponsListResponse(
        coupons=carousel_responses,
        total_count=len(carousel_responses)
    )

