from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from app.infra.db.postgres.repositories.restaurant_repository import RestaurantRepository
from app.infra.db.postgres.models.restaurant import Restaurant, RestaurantStatus
from app.infra.db.postgres.models.user import User, UserRole
from app.api.schemas.restaurant_schema import RestaurantCreateRequest, RestaurantUpdateRequest
from app.config.logger import get_logger

class RestaurantService:
    def __init__(self, db: Session):
        self.db = db
        self.restaurant_repository = RestaurantRepository(db)

    def create_restaurant(self, restaurant_data: RestaurantCreateRequest) -> Restaurant:
        """Create a new restaurant."""
        logger = get_logger(__name__)
        try:
            # Validate owner exists and has restaurant_owner role
            owner = self.db.query(User).filter(User.user_id == restaurant_data.owner_id).first()
            if not owner:
                raise ValueError("Owner user not found")
            
            if owner.role != UserRole.restaurant_owner:
                raise ValueError("User must have restaurant_owner role to create a restaurant")
            
            if owner.status.value != 'active':
                raise ValueError("Owner user must be active to create a restaurant")

            # Check if restaurant with same phone already exists
            existing_restaurant = self.restaurant_repository.get_restaurant_by_phone(restaurant_data.phone)
            if existing_restaurant:
                raise ValueError("Restaurant with this phone number already exists")
                
            # Check if restaurant with same email already exists (if email provided)
            if restaurant_data.email:
                existing_email = self.restaurant_repository.get_restaurant_by_email(restaurant_data.email)
                if existing_email:
                    raise ValueError("Restaurant with this email already exists")

            # Prepare restaurant data
            restaurant_dict = restaurant_data.model_dump()

            restaurant = self.restaurant_repository.create_restaurant(restaurant_dict)
            logger.info(f"Restaurant created successfully: {restaurant.restaurant_id}")
            return restaurant

        except ValueError as e:
            logger.warning(f"Restaurant creation validation error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error creating restaurant: {str(e)}")
            raise

    def get_restaurant_by_id(self, restaurant_id: UUID) -> Optional[Restaurant]:
        """Get restaurant by ID."""
        logger = get_logger(__name__)
        try:
            restaurant = self.restaurant_repository.get_restaurant_by_id(restaurant_id)
            if not restaurant:
                logger.warning(f"Restaurant not found: {restaurant_id}")
            return restaurant
        except Exception as e:
            logger.error(f"Error retrieving restaurant: {str(e)}")
            raise

    def get_restaurants_by_owner(self, owner_id: UUID) -> List[Restaurant]:
        """Get all restaurants owned by a specific user."""
        logger = get_logger(__name__)
        try:
            # First validate that the owner exists
            owner = self.db.query(User).filter(User.user_id == owner_id).first()
            if not owner:
                logger.warning(f"Owner user not found: {owner_id}")
                return []
            
            restaurants = self.restaurant_repository.get_restaurants_by_owner(owner_id)
            logger.info(f"Retrieved {len(restaurants)} restaurants for owner {owner_id}")
            return restaurants
        except Exception as e:
            logger.error(f"Error retrieving restaurants for owner: {str(e)}")
            raise

    def update_restaurant(self, restaurant_id: UUID, update_data: RestaurantUpdateRequest) -> Optional[Restaurant]:
        """Update restaurant information."""
        logger = get_logger(__name__)
        try:
            # Convert Pydantic model to dict, excluding None values
            update_dict = update_data.model_dump(exclude_unset=True, exclude_none=True)
            
            if not update_dict:
                raise ValueError("No data provided for update")

            # Check if phone number is being updated and if it already exists
            if 'phone' in update_dict:
                existing_restaurant = self.restaurant_repository.get_restaurant_by_phone(update_dict['phone'])
                if existing_restaurant and existing_restaurant.restaurant_id != restaurant_id:
                    raise ValueError("Restaurant with this phone number already exists")

            # Check if email is being updated and if it already exists
            if 'email' in update_dict and update_dict['email']:
                existing_email = self.restaurant_repository.get_restaurant_by_email(update_dict['email'])
                if existing_email and existing_email.restaurant_id != restaurant_id:
                    raise ValueError("Restaurant with this email already exists")

            restaurant = self.restaurant_repository.update_restaurant(restaurant_id, update_dict)
            if restaurant:
                logger.info(f"Restaurant updated successfully: {restaurant_id}")
            return restaurant

        except ValueError as e:
            logger.warning(f"Restaurant update validation error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error updating restaurant: {str(e)}")
            raise

    def delete_restaurant(self, restaurant_id: UUID) -> bool:
        """Soft delete restaurant."""
        logger = get_logger(__name__)
        try:
            result = self.restaurant_repository.delete_restaurant(restaurant_id)
            if result:
                logger.info(f"Restaurant deleted successfully: {restaurant_id}")
            return result
        except Exception as e:
            logger.error(f"Error deleting restaurant: {str(e)}")
            raise

    def get_all_restaurants(self, skip: int = 0, limit: int = 100, 
                          status: Optional[str] = None,
                          cuisine_type: Optional[str] = None,
                          city: Optional[str] = None,
                          is_open: Optional[bool] = None) -> List[Restaurant]:
        """Get all restaurants with optional filtering."""
        logger = get_logger(__name__)
        try:
            # Convert string enum to enum type if provided
            status_enum = RestaurantStatus(status) if status else None
            
            restaurants = self.restaurant_repository.get_all_restaurants(
                skip=skip, 
                limit=limit, 
                status=status_enum,
                cuisine_type=cuisine_type,
                city=city,
                is_open=is_open
            )
            logger.info(f"Retrieved {len(restaurants)} restaurants")
            return restaurants
        except ValueError as e:
            logger.warning(f"Invalid enum value: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error retrieving restaurants: {str(e)}")
            raise

    def search_restaurants_by_location(self, latitude: float, longitude: float, 
                                     radius_km: float = 10.0) -> List[Restaurant]:
        """Search restaurants within a certain radius of given coordinates."""
        logger = get_logger(__name__)
        try:
            restaurants = self.restaurant_repository.search_restaurants_by_location(
                latitude, longitude, radius_km
            )
            logger.info(f"Found {len(restaurants)} restaurants within {radius_km}km")
            return restaurants
        except Exception as e:
            logger.error(f"Error searching restaurants by location: {str(e)}")
            raise

    def update_restaurant_rating(self, restaurant_id: UUID, new_rating: float) -> bool:
        """Update restaurant rating."""
        logger = get_logger(__name__)
        try:
            if not 1 <= new_rating <= 5:
                raise ValueError("Rating must be between 1 and 5")
                
            result = self.restaurant_repository.update_restaurant_rating(restaurant_id, new_rating)
            if result:
                logger.info(f"Restaurant rating updated successfully: {restaurant_id}")
            return result
        except ValueError as e:
            logger.warning(f"Rating validation error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error updating restaurant rating: {str(e)}")
            raise

    def toggle_restaurant_status(self, restaurant_id: UUID) -> bool:
        """Toggle restaurant open/closed status."""
        logger = get_logger(__name__)
        try:
            result = self.restaurant_repository.toggle_restaurant_status(restaurant_id)
            if result:
                logger.info(f"Restaurant status toggled successfully: {restaurant_id}")
            return result
        except Exception as e:
            logger.error(f"Error toggling restaurant status: {str(e)}")
            raise

    def get_restaurant_statistics(self, restaurant_id: UUID) -> Dict[str, Any]:
        """Get restaurant statistics."""
        logger = get_logger(__name__)
        try:
            restaurant = self.restaurant_repository.get_restaurant_by_id(restaurant_id)
            if not restaurant:
                raise ValueError("Restaurant not found")
                
            stats = {
                "restaurant_id": str(restaurant.restaurant_id),
                "name": restaurant.name,
                "rating": float(restaurant.rating),
                "total_ratings": restaurant.total_ratings,
                "status": restaurant.status.value,
                "is_open": restaurant.is_open,
                "avg_delivery_time": restaurant.avg_delivery_time,
                "min_order_amount": float(restaurant.min_order_amount),
                "delivery_fee": float(restaurant.delivery_fee)
            }
            
            logger.info(f"Retrieved statistics for restaurant: {restaurant_id}")
            return stats
        except ValueError as e:
            logger.warning(f"Statistics validation error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error retrieving restaurant statistics: {str(e)}")
            raise 