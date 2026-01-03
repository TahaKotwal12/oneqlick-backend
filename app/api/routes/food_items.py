from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from datetime import datetime, timezone

from app.infra.db.postgres.postgres_config import get_db
from app.api.dependencies import get_optional_current_user
from app.api.schemas.common_schemas import CommonResponse
from app.infra.db.postgres.models.food_item import FoodItem
from app.infra.db.postgres.models.restaurant import Restaurant
from app.infra.db.postgres.models.restaurant_offer import RestaurantOffer
from app.infra.db.postgres.models.category import Category
from app.infra.db.postgres.models.user import User
from app.config.logger import get_logger

router = APIRouter(prefix="/food-items", tags=["food-items"])
logger = get_logger(__name__)


@router.get("/{food_item_id}", response_model=CommonResponse[dict])
async def get_food_item_by_id(
    food_item_id: str,
    include_restaurant: bool = Query(True, description="Include restaurant details"),
    include_customizations: bool = Query(True, description="Include customization options"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Get food item details by ID.
    
    This endpoint returns detailed information about a specific food item,
    including restaurant details, customization options, and nutritional information.
    """
    try:
        logger.info(f"Fetching food item details for ID: {food_item_id}")
        
        # Get food item from database
        food_item = db.query(FoodItem).filter(
            FoodItem.food_item_id == food_item_id,
            FoodItem.status == 'available'
        ).first()
        
        if not food_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Food item not found"
            )
        
        # Build food item response
        food_item_data = {
            'food_item_id': food_item.food_item_id,
            'name': food_item.name,
            'description': food_item.description,
            'price': float(food_item.price),
            'discount_price': float(food_item.discount_price) if food_item.discount_price else None,
            'image': food_item.image,
            'is_veg': food_item.is_veg,
            'ingredients': food_item.ingredients,
            'allergens': food_item.allergens,
            'calories': food_item.calories,
            'prep_time': food_item.prep_time,
            'preparation_time': food_item.preparation_time,
            'status': food_item.status,
            'rating': float(food_item.rating or 0),
            'total_ratings': food_item.total_ratings or 0,
            'is_popular': food_item.is_popular,
            'is_recommended': food_item.is_recommended,
            'nutrition_info': food_item.nutrition_info,
            'created_at': food_item.created_at,
            'updated_at': food_item.updated_at
        }
        
        # Include restaurant details if requested
        if include_restaurant:
            restaurant = db.query(Restaurant).filter(
                Restaurant.restaurant_id == food_item.restaurant_id,
                Restaurant.status == 'active'
            ).first()
            
            if restaurant:
                # Fetch active offers for this restaurant
                offers = db.query(RestaurantOffer).filter(
                    RestaurantOffer.restaurant_id == restaurant.restaurant_id,
                    RestaurantOffer.is_active == True,
                    RestaurantOffer.valid_from <= datetime.now(timezone.utc),
                    RestaurantOffer.valid_until >= datetime.now(timezone.utc)
                ).all()
                
                # Build offer responses
                offer_responses = [
                    {
                        'offer_id': str(offer.offer_id),
                        'title': offer.title,
                        'description': offer.description,
                        'discount_type': offer.discount_type,
                        'discount_value': float(offer.discount_value),
                        'min_order_amount': float(offer.min_order_amount) if offer.min_order_amount else None,
                        'max_discount_amount': float(offer.max_discount_amount) if offer.max_discount_amount else None,
                        'valid_from': offer.valid_from.isoformat(),
                        'valid_until': offer.valid_until.isoformat(),
                        'is_active': offer.is_active
                    } for offer in offers
                ]
                
                food_item_data['restaurant'] = {
                    'restaurant_id': restaurant.restaurant_id,
                    'name': restaurant.name,
                    'description': restaurant.description,
                    'cuisine_type': restaurant.cuisine_type,
                    'image': restaurant.image,
                    'rating': float(restaurant.rating or 0),
                    'total_ratings': restaurant.total_ratings or 0,
                    'avg_delivery_time': restaurant.avg_delivery_time,
                    'delivery_fee': float(restaurant.delivery_fee or 0),
                    'min_order_amount': float(restaurant.min_order_amount or 0),
                    'is_open': restaurant.is_open,
                    'is_veg': restaurant.is_veg,
                    'is_pure_veg': restaurant.is_pure_veg,
                    'phone': restaurant.phone,
                    'email': restaurant.email,
                    'address_line1': restaurant.address_line1,
                    'address_line2': restaurant.address_line2,
                    'city': restaurant.city,
                    'state': restaurant.state,
                    'postal_code': restaurant.postal_code,
                    'latitude': float(restaurant.latitude),
                    'longitude': float(restaurant.longitude),
                    'offers': offer_responses  # Add offers here
                }
        
        # Include category details
        if food_item.category_id:
            category = db.query(Category).filter(
                Category.category_id == food_item.category_id,
                Category.is_active == True
            ).first()
            
            if category:
                food_item_data['category'] = {
                    'category_id': category.category_id,
                    'name': category.name,
                    'description': category.description,
                    'image': category.image
                }
        
        # Include customization options if requested
        if include_customizations:
            # For now, we'll return empty customization options
            # This can be expanded later when customization tables are properly set up
            food_item_data['customizations'] = {
                'size_options': [],
                'addon_options': [],
                'beverage_options': []
            }
        
        logger.info(f"Food item details retrieved successfully for: {food_item.name}")
        
        return CommonResponse(
            code=200,
            message="Food item details retrieved successfully",
            message_id="FOOD_ITEM_DETAILS_SUCCESS",
            data=food_item_data
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching food item details: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch food item details: {str(e)}"
        )


@router.get("/", response_model=CommonResponse[dict])
async def get_food_items(
    restaurant_id: Optional[str] = Query(None, description="Filter by restaurant ID"),
    category_id: Optional[str] = Query(None, description="Filter by category ID"),
    is_veg: Optional[bool] = Query(None, description="Filter by vegetarian items"),
    is_popular: Optional[bool] = Query(None, description="Filter by popular items"),
    is_recommended: Optional[bool] = Query(None, description="Filter by recommended items"),
    limit: int = Query(20, ge=1, le=100, description="Number of items to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Get list of food items with optional filters.
    
    This endpoint returns a paginated list of food items with various filtering options.
    """
    try:
        logger.info("Fetching food items list")
        
        # Base query
        query = db.query(FoodItem).filter(FoodItem.status == 'available')
        
        # Apply filters
        if restaurant_id:
            query = query.filter(FoodItem.restaurant_id == restaurant_id)
        
        if category_id:
            query = query.filter(FoodItem.category_id == category_id)
        
        if is_veg is not None:
            query = query.filter(FoodItem.is_veg == is_veg)
        
        if is_popular is not None:
            query = query.filter(FoodItem.is_popular == is_popular)
        
        if is_recommended is not None:
            query = query.filter(FoodItem.is_recommended == is_recommended)
        
        # Get total count
        total_count = query.count()
        
        # Apply pagination and ordering
        food_items = query.order_by(
            FoodItem.is_popular.desc(),
            FoodItem.is_recommended.desc(),
            FoodItem.rating.desc(),
            FoodItem.created_at.desc()
        ).offset(offset).limit(limit).all()
        
        # Build response
        food_items_data = []
        for item in food_items:
            food_items_data.append({
                'food_item_id': item.food_item_id,
                'name': item.name,
                'description': item.description,
                'price': float(item.price),
                'discount_price': float(item.discount_price) if item.discount_price else None,
                'image': item.image,
                'is_veg': item.is_veg,
                'rating': float(item.rating or 0),
                'total_ratings': item.total_ratings or 0,
                'is_popular': item.is_popular,
                'is_recommended': item.is_recommended,
                'prep_time': item.prep_time,
                'calories': item.calories,
                'restaurant_id': item.restaurant_id,
                'category_id': item.category_id
            })
        
        # Check if there are more results
        has_more = (offset + limit) < total_count
        
        logger.info(f"Found {total_count} food items, returning {len(food_items_data)}")
        
        return CommonResponse(
            code=200,
            message="Food items retrieved successfully",
            message_id="FOOD_ITEMS_SUCCESS",
            data={
                'food_items': food_items_data,
                'total_count': total_count,
                'has_more': has_more,
                'offset': offset,
                'limit': limit
            }
        )
    
    except Exception as e:
        logger.error(f"Error fetching food items: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch food items: {str(e)}"
        )
