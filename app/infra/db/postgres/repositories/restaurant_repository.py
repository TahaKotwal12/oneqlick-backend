from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from app.infra.db.postgres.models.restaurant import Restaurant, RestaurantStatus
from app.config.logger import get_logger

logger = get_logger(__name__)

class RestaurantRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_restaurant(self, restaurant_data: dict) -> Restaurant:
        """Create a new restaurant in the database."""
        try:
            # Ensure timestamps are set
            current_time = datetime.utcnow()
            restaurant_data.setdefault('created_at', current_time)
            restaurant_data.setdefault('updated_at', current_time)
            
            restaurant = Restaurant(**restaurant_data)
            self.db.add(restaurant)
            self.db.commit()
            self.db.refresh(restaurant)
            logger.info(f"Restaurant created successfully with ID: {restaurant.restaurant_id}")
            return restaurant
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Integrity error creating restaurant: {str(e)}")
            raise ValueError("Restaurant with this information already exists")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating restaurant: {str(e)}")
            raise

    def get_restaurant_by_id(self, restaurant_id: UUID) -> Optional[Restaurant]:
        """Get restaurant by ID."""
        try:
            restaurant = self.db.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id).first()
            if restaurant:
                logger.info(f"Restaurant retrieved successfully: {restaurant_id}")
            else:
                logger.warning(f"Restaurant not found: {restaurant_id}")
            return restaurant
        except Exception as e:
            logger.error(f"Error retrieving restaurant by ID {restaurant_id}: {str(e)}")
            raise

    def get_restaurant_by_phone(self, phone: str) -> Optional[Restaurant]:
        """Get restaurant by phone number."""
        try:
            restaurant = self.db.query(Restaurant).filter(Restaurant.phone == phone).first()
            return restaurant
        except Exception as e:
            logger.error(f"Error retrieving restaurant by phone {phone}: {str(e)}")
            raise

    def get_restaurant_by_email(self, email: str) -> Optional[Restaurant]:
        """Get restaurant by email."""
        try:
            restaurant = self.db.query(Restaurant).filter(Restaurant.email == email).first()
            return restaurant
        except Exception as e:
            logger.error(f"Error retrieving restaurant by email {email}: {str(e)}")
            raise

    def get_restaurants_by_owner(self, owner_id: UUID) -> List[Restaurant]:
        """Get all restaurants owned by a specific user."""
        try:
            restaurants = self.db.query(Restaurant).filter(Restaurant.owner_id == owner_id).all()
            logger.info(f"Retrieved {len(restaurants)} restaurants for owner {owner_id}")
            return restaurants
        except Exception as e:
            logger.error(f"Error retrieving restaurants for owner {owner_id}: {str(e)}")
            raise

    def update_restaurant(self, restaurant_id: UUID, update_data: dict) -> Optional[Restaurant]:
        """Update restaurant information."""
        try:
            restaurant = self.db.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id).first()
            if not restaurant:
                logger.warning(f"Restaurant not found for update: {restaurant_id}")
                return None

            # Set updated_at timestamp
            update_data['updated_at'] = datetime.utcnow()

            for key, value in update_data.items():
                if hasattr(restaurant, key) and value is not None:
                    setattr(restaurant, key, value)

            self.db.commit()
            self.db.refresh(restaurant)
            logger.info(f"Restaurant updated successfully: {restaurant_id}")
            return restaurant
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Integrity error updating restaurant: {str(e)}")
            raise ValueError("Restaurant with this information already exists")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating restaurant {restaurant_id}: {str(e)}")
            raise

    def delete_restaurant(self, restaurant_id: UUID) -> bool:
        """Soft delete restaurant by setting status to inactive."""
        try:
            restaurant = self.db.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id).first()
            if not restaurant:
                logger.warning(f"Restaurant not found for deletion: {restaurant_id}")
                return False

            restaurant.status = RestaurantStatus.inactive
            self.db.commit()
            logger.info(f"Restaurant soft deleted successfully: {restaurant_id}")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting restaurant {restaurant_id}: {str(e)}")
            raise

    def get_all_restaurants(self, skip: int = 0, limit: int = 100, 
                          status: Optional[RestaurantStatus] = None,
                          cuisine_type: Optional[str] = None,
                          city: Optional[str] = None,
                          is_open: Optional[bool] = None) -> List[Restaurant]:
        """Get all restaurants with optional filtering."""
        try:
            query = self.db.query(Restaurant)
            
            if status:
                query = query.filter(Restaurant.status == status)
            if cuisine_type:
                query = query.filter(Restaurant.cuisine_type == cuisine_type)
            if city:
                query = query.filter(Restaurant.city.ilike(f"%{city}%"))
            if is_open is not None:
                query = query.filter(Restaurant.is_open == is_open)
                
            restaurants = query.offset(skip).limit(limit).all()
            logger.info(f"Retrieved {len(restaurants)} restaurants")
            return restaurants
        except Exception as e:
            logger.error(f"Error retrieving restaurants: {str(e)}")
            raise

    def search_restaurants_by_location(self, latitude: float, longitude: float, 
                                     radius_km: float = 10.0) -> List[Restaurant]:
        """Search restaurants within a certain radius of given coordinates."""
        try:
            # Using Haversine formula to calculate distance
            # This is a simplified version - for production, consider using PostGIS
            query = self.db.query(Restaurant).filter(
                Restaurant.status == RestaurantStatus.active
            )
            
            restaurants = query.all()
            
            # Filter by distance (simplified calculation)
            # In production, use PostGIS for better performance
            nearby_restaurants = []
            for restaurant in restaurants:
                # Simple distance calculation (approximate)
                lat_diff = abs(float(restaurant.latitude) - latitude)
                lon_diff = abs(float(restaurant.longitude) - longitude)
                
                # Rough conversion to km (1 degree ≈ 111 km)
                distance_km = ((lat_diff ** 2 + lon_diff ** 2) ** 0.5) * 111
                
                if distance_km <= radius_km:
                    nearby_restaurants.append(restaurant)
            
            logger.info(f"Found {len(nearby_restaurants)} restaurants within {radius_km}km")
            return nearby_restaurants
        except Exception as e:
            logger.error(f"Error searching restaurants by location: {str(e)}")
            raise

    def update_restaurant_rating(self, restaurant_id: UUID, new_rating: float) -> bool:
        """Update restaurant rating and total ratings count."""
        try:
            restaurant = self.db.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id).first()
            if not restaurant:
                return False
                
            # Update rating calculation
            current_total = restaurant.rating * restaurant.total_ratings
            restaurant.total_ratings += 1
            restaurant.rating = (current_total + new_rating) / restaurant.total_ratings
            
            self.db.commit()
            logger.info(f"Updated rating for restaurant {restaurant_id}: {restaurant.rating}")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating restaurant rating {restaurant_id}: {str(e)}")
            raise

    def toggle_restaurant_status(self, restaurant_id: UUID) -> bool:
        """Toggle restaurant open/closed status."""
        try:
            restaurant = self.db.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id).first()
            if not restaurant:
                return False
                
            restaurant.is_open = not restaurant.is_open
            self.db.commit()
            logger.info(f"Toggled restaurant status {restaurant_id}: {restaurant.is_open}")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error toggling restaurant status {restaurant_id}: {str(e)}")
            raise 