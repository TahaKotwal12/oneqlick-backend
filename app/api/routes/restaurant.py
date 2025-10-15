from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timezone
from decimal import Decimal
import math

from app.infra.db.postgres.postgres_config import get_db
from app.api.dependencies import get_optional_current_user
from app.api.schemas.restaurant_schemas import (
    NearbyRestaurantsResponse,
    RestaurantResponse,
    RestaurantLocationResponse,
    RestaurantOfferResponse,
    PopularDishesResponse,
    PopularDishResponse,
    RestaurantBasicResponse,
    RestaurantDetailResponse,
    MenuItemResponse,
    MenuCategoryResponse,
    RestaurantMenuResponse
)
from app.api.schemas.common_schemas import CommonResponse
from app.infra.db.postgres.models.restaurant import Restaurant
from app.infra.db.postgres.models.restaurant_offer import RestaurantOffer
from app.infra.db.postgres.models.food_item import FoodItem
from app.infra.db.postgres.models.category import Category
from app.infra.db.postgres.models.user import User
from app.config.logger import get_logger

router = APIRouter(prefix="/restaurants", tags=["restaurants"])
logger = get_logger(__name__)


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two points using Haversine formula.
    Returns distance in kilometers.
    """
    # Earth's radius in kilometers
    R = 6371.0
    
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(float(lat2))
    lon2_rad = math.radians(float(lon2))
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return round(distance, 2)


def is_restaurant_currently_open(restaurant: Restaurant) -> bool:
    """
    Check if restaurant is currently open based on opening/closing hours.
    Handles midnight crossover.
    """
    if not restaurant.is_open:
        return False
    
    if restaurant.opening_time is None or restaurant.closing_time is None:
        return True  # If no hours set, assume always open
    
    current_time = datetime.now().time()
    
    # Handle normal case (opening < closing)
    if restaurant.opening_time < restaurant.closing_time:
        return restaurant.opening_time <= current_time <= restaurant.closing_time
    else:
        # Handle midnight crossover (e.g., 22:00 to 02:00)
        return current_time >= restaurant.opening_time or current_time <= restaurant.closing_time


@router.get("/nearby", response_model=CommonResponse[NearbyRestaurantsResponse])
async def get_nearby_restaurants(
    latitude: float = Query(..., ge=-90, le=90, description="User's latitude"),
    longitude: float = Query(..., ge=-180, le=180, description="User's longitude"),
    radius_km: float = Query(5.0, ge=0.1, le=50, description="Search radius in kilometers"),
    limit: int = Query(10, ge=1, le=100, description="Number of restaurants to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    is_veg_only: Optional[bool] = Query(None, description="Filter for pure vegetarian restaurants"),
    is_open: Optional[bool] = Query(None, description="Filter for currently open restaurants"),
    sort_by: str = Query("distance", description="Sort by: distance, rating, delivery_time, cost_low, cost_high"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Get nearby restaurants based on user's location.
    
    This endpoint returns a list of restaurants within the specified radius,
    sorted by distance, rating, or other criteria. Includes active offers for each restaurant.
    """
    try:
        logger.info(f"Fetching nearby restaurants for location: ({latitude}, {longitude}), radius: {radius_km}km")
        
        # Validate sort_by parameter
        valid_sorts = ['distance', 'rating', 'delivery_time', 'cost_low', 'cost_high']
        if sort_by not in valid_sorts:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid sort_by value. Must be one of: {', '.join(valid_sorts)}"
            )
        
        # Base query for restaurants
        query = db.query(Restaurant).filter(
            Restaurant.status == 'active'
        )
        
        # Apply filters
        if is_veg_only is not None:
            query = query.filter(Restaurant.is_pure_veg == is_veg_only)
        
        # Get all restaurants (we'll filter by distance in Python)
        all_restaurants = query.all()
        
        # Calculate distances and filter by radius
        restaurants_with_distance = []
        for restaurant in all_restaurants:
            distance = calculate_distance(
                latitude,
                longitude,
                float(restaurant.latitude),
                float(restaurant.longitude)
            )
            
            # Filter by radius
            if distance <= radius_km:
                # Check if restaurant is currently open (if filter applied)
                currently_open = is_restaurant_currently_open(restaurant)
                
                if is_open is None or is_open == currently_open:
                    restaurants_with_distance.append((restaurant, distance, currently_open))
        
        # Sort restaurants
        if sort_by == "distance":
            restaurants_with_distance.sort(key=lambda x: x[1])
        elif sort_by == "rating":
            restaurants_with_distance.sort(key=lambda x: float(x[0].rating), reverse=True)
        elif sort_by == "delivery_time":
            restaurants_with_distance.sort(key=lambda x: x[0].avg_delivery_time or 999)
        elif sort_by == "cost_low":
            restaurants_with_distance.sort(key=lambda x: float(x[0].cost_for_two or 0))
        elif sort_by == "cost_high":
            restaurants_with_distance.sort(key=lambda x: float(x[0].cost_for_two or 0), reverse=True)
        
        # Get total count before pagination
        total_count = len(restaurants_with_distance)
        
        # Apply pagination
        paginated_restaurants = restaurants_with_distance[offset:offset + limit]
        
        # Build response
        restaurant_responses = []
        for restaurant, distance, currently_open in paginated_restaurants:
            # Fetch active offers for this restaurant
            offers = db.query(RestaurantOffer).filter(
                RestaurantOffer.restaurant_id == restaurant.restaurant_id,
                RestaurantOffer.is_active == True,
                RestaurantOffer.valid_from <= datetime.now(timezone.utc),
                RestaurantOffer.valid_until >= datetime.now(timezone.utc)
            ).all()
            
            # Build location response
            location = RestaurantLocationResponse(
                address_line1=restaurant.address_line1,
                address_line2=restaurant.address_line2,
                city=restaurant.city,
                state=restaurant.state,
                postal_code=restaurant.postal_code,
                latitude=restaurant.latitude,
                longitude=restaurant.longitude
            )
            
            # Build offer responses
            offer_responses = [
                RestaurantOfferResponse(
                    offer_id=offer.offer_id,
                    title=offer.title,
                    description=offer.description,
                    discount_type=offer.discount_type,
                    discount_value=offer.discount_value,
                    min_order_amount=offer.min_order_amount,
                    max_discount_amount=offer.max_discount_amount,
                    valid_from=offer.valid_from,
                    valid_until=offer.valid_until,
                    is_active=offer.is_active
                ) for offer in offers
            ]
            
            # Build restaurant response
            restaurant_dict = {
                'restaurant_id': restaurant.restaurant_id,
                'name': restaurant.name,
                'description': restaurant.description,
                'cuisine_type': restaurant.cuisine_type,
                'image': restaurant.image,
                'cover_image': restaurant.cover_image,
                'rating': restaurant.rating,
                'total_ratings': restaurant.total_ratings,
                'avg_delivery_time': restaurant.avg_delivery_time,
                'delivery_fee': restaurant.delivery_fee,
                'min_order_amount': restaurant.min_order_amount,
                'cost_for_two': restaurant.cost_for_two,
                'platform_fee': restaurant.platform_fee,
                'status': restaurant.status,
                'is_open': currently_open,
                'is_veg': restaurant.is_veg,
                'is_pure_veg': restaurant.is_pure_veg,
                'opening_time': restaurant.opening_time,
                'closing_time': restaurant.closing_time,
                'distance': distance,
                'location': location,
                'offers': offer_responses
            }
            
            restaurant_response = RestaurantResponse(**restaurant_dict)
            restaurant_responses.append(restaurant_response)
        
        # Check if there are more results
        has_more = (offset + limit) < total_count
        
        logger.info(f"Found {total_count} restaurants, returning {len(restaurant_responses)}")
        
        return CommonResponse(
            code=200,
            message="Nearby restaurants retrieved successfully",
            message_id="NEARBY_RESTAURANTS_SUCCESS",
            data=NearbyRestaurantsResponse(
                restaurants=restaurant_responses,
                total_count=total_count,
                has_more=has_more
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching nearby restaurants: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch nearby restaurants: {str(e)}"
        )


@router.get("/popular-dishes", response_model=CommonResponse[PopularDishesResponse])
async def get_popular_dishes(
    latitude: float = Query(..., ge=-90, le=90, description="User's latitude"),
    longitude: float = Query(..., ge=-180, le=180, description="User's longitude"),
    radius_km: float = Query(10.0, ge=0.1, le=50, description="Search radius in kilometers"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of dishes to return"),
    is_veg_only: Optional[bool] = Query(None, description="Filter for vegetarian dishes only"),
    category: Optional[str] = Query(None, description="Filter by food category"),
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Get popular dishes from nearby restaurants based on user's location.
    Returns dishes marked as popular from restaurants within the specified radius.
    """
    try:
        # Haversine formula for distance calculation
        def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
            R = 6371  # Earth's radius in kilometers
            dlat = math.radians(lat2 - lat1)
            dlon = math.radians(lon2 - lon1)
            a = (math.sin(dlat/2) * math.sin(dlat/2) + 
                 math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
                 math.sin(dlon/2) * math.sin(dlon/2))
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            return R * c

        # Get nearby restaurants first
        nearby_restaurants_query = db.query(Restaurant).filter(
            Restaurant.status == 'active'
        )
        
        # Calculate distance for each restaurant and filter by radius
        nearby_restaurants = []
        for restaurant in nearby_restaurants_query.all():
            if restaurant.latitude and restaurant.longitude:
                distance = calculate_distance(
                    latitude, longitude, 
                    float(restaurant.latitude), float(restaurant.longitude)
                )
                if distance <= radius_km:
                    restaurant.distance = distance
                    nearby_restaurants.append(restaurant)
        
        if not nearby_restaurants:
            return CommonResponse(
                code=200,
                message="No restaurants found within the specified radius",
                message_id="NO_RESTAURANTS_FOUND",
                data=PopularDishesResponse(
                    dishes=[],
                    total_count=0,
                    has_more=False
                )
            )
        
        # Get restaurant IDs
        restaurant_ids = [r.restaurant_id for r in nearby_restaurants]
        
        # Query popular dishes from nearby restaurants
        query = db.query(FoodItem).filter(
            FoodItem.restaurant_id.in_(restaurant_ids),
            FoodItem.status == 'available',
            FoodItem.is_popular == True
        )
        
        # Apply filters
        if is_veg_only is not None:
            query = query.filter(FoodItem.is_veg == is_veg_only)
        
        if category:
            query = query.join(Category, FoodItem.category_id == Category.category_id).filter(Category.name.ilike(f"%{category}%"))
        
        # Order by rating and total_ratings for popularity
        query = query.order_by(
            FoodItem.rating.desc(),
            FoodItem.total_ratings.desc(),
            FoodItem.created_at.desc()
        )
        
        # Get total count before pagination
        total_count = query.count()
        
        # Apply pagination
        dishes = query.offset(0).limit(limit).all()
        
        # Create a mapping of restaurant_id to restaurant for quick lookup
        restaurant_map = {r.restaurant_id: r for r in nearby_restaurants}
        
        # Get category names for dishes
        category_ids = [dish.category_id for dish in dishes if dish.category_id]
        categories = {}
        if category_ids:
            category_query = db.query(Category).filter(Category.category_id.in_(category_ids))
            categories = {cat.category_id: cat.name for cat in category_query.all()}
        
        # Transform dishes to include restaurant info and distance
        popular_dishes = []
        for dish in dishes:
            restaurant = restaurant_map.get(dish.restaurant_id)
            if restaurant:
                # Create restaurant basic response
                restaurant_basic = RestaurantBasicResponse(
                    restaurant_id=restaurant.restaurant_id,
                    name=restaurant.name,
                    cuisine_type=restaurant.cuisine_type,
                    rating=restaurant.rating or Decimal('0.0'),
                    total_ratings=restaurant.total_ratings or 0,
                    avg_delivery_time=restaurant.avg_delivery_time,
                    image=restaurant.image,
                    is_open=restaurant.is_open,
                    is_veg=restaurant.is_veg,
                    is_pure_veg=restaurant.is_pure_veg
                )
                
                # Create popular dish response
                popular_dish = PopularDishResponse(
                    food_item_id=dish.food_item_id,
                    name=dish.name,
                    description=dish.description,
                    price=dish.price,
                    discount_price=dish.discount_price,
                    image=dish.image,
                    is_veg=dish.is_veg,
                    is_popular=dish.is_popular,
                    is_recommended=dish.is_recommended,
                    rating=dish.rating or Decimal('0.0'),
                    total_ratings=dish.total_ratings or 0,
                    prep_time=dish.prep_time,
                    calories=dish.calories,
                    category=categories.get(dish.category_id, 'General'),
                    restaurant=restaurant_basic,
                    distance=restaurant.distance
                )
                popular_dishes.append(popular_dish)
        
        # Check if there are more dishes
        has_more = total_count > limit
        
        return CommonResponse(
            code=200,
            message=f"Found {len(popular_dishes)} popular dishes from nearby restaurants",
            message_id="POPULAR_DISHES_SUCCESS",
            data=PopularDishesResponse(
                dishes=popular_dishes,
                total_count=total_count,
                has_more=has_more
            )
        )
        
    except Exception as e:
        logger.error(f"Error fetching popular dishes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch popular dishes: {str(e)}"
        )


@router.get("/{restaurant_id}", response_model=CommonResponse[RestaurantDetailResponse])
async def get_restaurant_by_id(
    restaurant_id: str,
    include_menu: bool = Query(False, description="Include menu items"),
    include_reviews: bool = Query(False, description="Include reviews"),
    include_offers: bool = Query(True, description="Include active offers"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Get restaurant details by ID.
    
    This endpoint returns detailed information about a specific restaurant,
    including contact information, location, offers, and optionally menu items and reviews.
    """
    try:
        logger.info(f"Fetching restaurant details for ID: {restaurant_id}")
        
        # Get restaurant from database
        restaurant = db.query(Restaurant).filter(
            Restaurant.restaurant_id == restaurant_id,
            Restaurant.status == 'active'
        ).first()
        
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )
        
        # Check if restaurant is currently open
        currently_open = is_restaurant_currently_open(restaurant)
        
        # Build location response
        location = RestaurantLocationResponse(
            address_line1=restaurant.address_line1,
            address_line2=restaurant.address_line2,
            city=restaurant.city,
            state=restaurant.state,
            postal_code=restaurant.postal_code,
            latitude=restaurant.latitude,
            longitude=restaurant.longitude
        )
        
        # Fetch active offers if requested
        offers = []
        if include_offers:
            offers = db.query(RestaurantOffer).filter(
                RestaurantOffer.restaurant_id == restaurant.restaurant_id,
                RestaurantOffer.is_active == True,
                RestaurantOffer.valid_from <= datetime.now(timezone.utc),
                RestaurantOffer.valid_until >= datetime.now(timezone.utc)
            ).all()
        
        # Build offer responses
        offer_responses = [
            RestaurantOfferResponse(
                offer_id=offer.offer_id,
                title=offer.title,
                description=offer.description,
                discount_type=offer.discount_type,
                discount_value=offer.discount_value,
                min_order_amount=offer.min_order_amount,
                max_discount_amount=offer.max_discount_amount,
                valid_from=offer.valid_from,
                valid_until=offer.valid_until,
                is_active=offer.is_active
            ) for offer in offers
        ]
        
        # Fetch menu data if requested
        menu_data = None
        if include_menu:
            # Get all food items for this restaurant
            food_items = db.query(FoodItem).filter(
                FoodItem.restaurant_id == restaurant.restaurant_id,
                FoodItem.status == 'available'
            ).order_by(FoodItem.sort_order, FoodItem.name).all()
            
            # Get all categories for this restaurant
            category_ids = list(set([item.category_id for item in food_items if item.category_id]))
            categories = db.query(Category).filter(
                Category.category_id.in_(category_ids),
                Category.is_active == True
            ).order_by(Category.sort_order, Category.name).all()
            
            # Create category map for quick lookup
            category_map = {cat.category_id: cat for cat in categories}
            
            # Group food items by category
            menu_categories = []
            total_items = 0
            
            for category in categories:
                category_items = [item for item in food_items if item.category_id == category.category_id]
                if category_items:  # Only include categories that have items
                    # Transform food items to response format
                    menu_items = []
                    for item in category_items:
                        menu_item = MenuItemResponse(
                            food_item_id=item.food_item_id,
                            name=item.name,
                            description=item.description,
                            price=item.price,
                            discount_price=item.discount_price,
                            image=item.image,
                            is_veg=item.is_veg,
                            ingredients=item.ingredients,
                            allergens=item.allergens,
                            calories=item.calories,
                            prep_time=item.prep_time,
                            status=item.status,
                            rating=item.rating,
                            total_ratings=item.total_ratings,
                            is_popular=item.is_popular,
                            is_recommended=item.is_recommended,
                            nutrition_info=item.nutrition_info,
                            preparation_time=item.preparation_time,
                            category=category.name
                        )
                        menu_items.append(menu_item)
                        total_items += 1
                    
                    # Create category response
                    menu_category = MenuCategoryResponse(
                        category_id=category.category_id,
                        name=category.name,
                        description=category.description,
                        image=category.image,
                        is_active=category.is_active,
                        sort_order=category.sort_order,
                        items=menu_items
                    )
                    menu_categories.append(menu_category)
            
            # Create menu response
            menu_data = RestaurantMenuResponse(
                categories=menu_categories,
                total_items=total_items
            )
        
        # Build restaurant response
        restaurant_dict = {
            'restaurant_id': restaurant.restaurant_id,
            'name': restaurant.name,
            'description': restaurant.description,
            'cuisine_type': restaurant.cuisine_type,
            'image': restaurant.image,
            'cover_image': restaurant.cover_image,
            'rating': restaurant.rating,
            'total_ratings': restaurant.total_ratings,
            'avg_delivery_time': restaurant.avg_delivery_time,
            'delivery_fee': restaurant.delivery_fee,
            'min_order_amount': restaurant.min_order_amount,
            'cost_for_two': restaurant.cost_for_two,
            'platform_fee': restaurant.platform_fee,
            'status': restaurant.status,
            'is_open': currently_open,
            'is_veg': restaurant.is_veg,
            'is_pure_veg': restaurant.is_pure_veg,
            'opening_time': restaurant.opening_time,
            'closing_time': restaurant.closing_time,
            'location': location,
            'offers': offer_responses,
            'phone': restaurant.phone,
            'email': restaurant.email,
            'created_at': restaurant.created_at,
            'updated_at': restaurant.updated_at,
            'menu': menu_data
        }
        
        restaurant_response = RestaurantDetailResponse(**restaurant_dict)
        
        logger.info(f"Restaurant details retrieved successfully for: {restaurant.name}")
        
        return CommonResponse(
            code=200,
            message="Restaurant details retrieved successfully",
            message_id="RESTAURANT_DETAILS_SUCCESS",
            data=restaurant_response
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching restaurant details: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch restaurant details: {str(e)}"
        )
