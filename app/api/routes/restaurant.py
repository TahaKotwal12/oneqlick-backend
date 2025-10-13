from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timezone
import math

from app.infra.db.postgres.postgres_config import get_db
from app.api.dependencies import get_optional_current_user
from app.api.schemas.restaurant_schemas import (
    NearbyRestaurantsResponse,
    RestaurantResponse,
    RestaurantLocationResponse,
    RestaurantOfferResponse
)
from app.api.schemas.common_schemas import CommonResponse
from app.infra.db.postgres.models.restaurant import Restaurant
from app.infra.db.postgres.models.restaurant_offer import RestaurantOffer
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

