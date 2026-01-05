"""
Production-grade search service using PostgreSQL Full-Text Search and fuzzy matching.
Optimized for Railway deployment with NeonDB.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_, text
from typing import List, Dict, Any, Optional, Tuple
import time
from decimal import Decimal
import math

from app.infra.db.postgres.models.restaurant import Restaurant
from app.infra.db.postgres.models.food_item import FoodItem
from app.infra.db.postgres.models.category import Category
from app.infra.db.postgres.models.search import SearchHistory
from app.config.logger import get_logger

logger = get_logger(__name__)


class SearchService:
    """
    Production-grade search service with PostgreSQL FTS and fuzzy matching.
    
    Features:
    - Full-text search with tsvector
    - Fuzzy matching using pg_trgm
    - Weighted relevance scoring
    - Location-based filtering
    - Search analytics tracking
    """
    
    def __init__(self, db: Session):
        self.db = db
        
    def unified_search(
        self,
        query: str,
        latitude: float,
        longitude: float,
        radius_km: float = 10.0,
        search_type: str = "all",
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 20,
        offset: int = 0,
        use_fuzzy: bool = True
    ) -> Dict[str, Any]:
        """
        Unified search across restaurants, dishes, and categories.
        
        Args:
            query: Search query string
            latitude: User's latitude
            longitude: User's longitude
            radius_km: Search radius in kilometers
            search_type: 'all', 'restaurants', 'dishes', or 'categories'
            filters: Additional filters (is_veg_only, is_open, etc.)
            limit: Maximum results to return
            offset: Pagination offset
            use_fuzzy: Enable fuzzy matching for typo tolerance
            
        Returns:
            Dictionary with results, total_count, and metadata
        """
        start_time = time.time()
        filters = filters or {}
        
        logger.info(f"Search query: '{query}', type: {search_type}, location: ({latitude}, {longitude})")
        
        # Initialize results
        all_results = []
        
        # Search restaurants
        if search_type in ['all', 'restaurants']:
            restaurant_results = self._search_restaurants_fts(
                query, latitude, longitude, radius_km, filters, use_fuzzy
            )
            all_results.extend(restaurant_results)
        
        # Search dishes
        if search_type in ['all', 'dishes']:
            # Get nearby restaurant IDs first
            nearby_restaurant_ids = self._get_nearby_restaurant_ids(
                latitude, longitude, radius_km
            )
            
            if nearby_restaurant_ids:
                dish_results = self._search_dishes_fts(
                    query, nearby_restaurant_ids, filters, use_fuzzy
                )
                all_results.extend(dish_results)
        
        # Search categories
        if search_type in ['all', 'categories']:
            category_results = self._search_categories_fts(query, use_fuzzy)
            all_results.extend(category_results)
        
        # Sort by relevance score
        all_results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        # Apply pagination
        total_count = len(all_results)
        paginated_results = all_results[offset:offset + limit]
        
        execution_time = (time.time() - start_time) * 1000  # Convert to ms
        
        logger.info(f"Search completed: {total_count} results in {execution_time:.2f}ms")
        
        return {
            'results': paginated_results,
            'total_count': total_count,
            'has_more': (offset + limit) < total_count,
            'execution_time_ms': round(execution_time, 2),
            'search_query': query,
            'search_type': search_type
        }
    
    def _search_restaurants_fts(
        self,
        query: str,
        latitude: float,
        longitude: float,
        radius_km: float,
        filters: Dict[str, Any],
        use_fuzzy: bool
    ) -> List[Dict[str, Any]]:
        """Search restaurants using FTS, fuzzy matching, and trigram prefix matching."""
        
        # Prepare tsquery for full-text search
        tsquery = func.plainto_tsquery('english', query)
        
        # Base query with FTS ranking
        base_query = self.db.query(
            Restaurant,
            func.ts_rank(Restaurant.search_vector, tsquery).label('fts_rank'),
            func.similarity(Restaurant.name, query).label('name_similarity'),
            func.similarity(Restaurant.cuisine_type, query).label('cuisine_similarity')
        ).filter(
            Restaurant.status == 'active'
        )
        
        # Apply FTS + trigram matching (production-grade)
        if use_fuzzy:
            # Use lower similarity threshold (0.1) for prefix matching
            # This allows "bir" to match "biryani" using trigrams (indexed!)
            base_query = base_query.filter(
                or_(
                    Restaurant.search_vector.op('@@')(tsquery),  # Full-text search (indexed)
                    func.similarity(Restaurant.name, query) > 0.1,  # Trigram prefix match (indexed)
                    func.similarity(Restaurant.cuisine_type, query) > 0.1,  # Trigram cuisine (indexed)
                    func.similarity(Restaurant.description, query) > 0.15  # Trigram description (indexed)
                )
            )
        else:
            # Pure FTS
            base_query = base_query.filter(
                Restaurant.search_vector.op('@@')(tsquery)
            )
        
        # Apply filters
        if filters.get('is_veg_only'):
            base_query = base_query.filter(Restaurant.is_pure_veg == True)
        
        # Execute query
        restaurants = base_query.all()
        
        # Calculate distances and filter by radius
        results = []
        for restaurant, fts_rank, name_similarity in restaurants:
            distance = self._calculate_distance(
                latitude, longitude,
                float(restaurant.latitude), float(restaurant.longitude)
            )
            
            if distance <= radius_km:
                # Check if restaurant is currently open
                is_open = self._is_restaurant_open(restaurant)
                
                # Apply open filter if specified
                if filters.get('is_open') is None or filters.get('is_open') == is_open:
                    # Calculate combined relevance score
                    relevance = self._calculate_restaurant_relevance(
                        fts_rank, name_similarity, distance, restaurant
                    )
                    
                    results.append({
                        'type': 'restaurant',
                        'id': str(restaurant.restaurant_id),
                        'name': restaurant.name,
                        'description': restaurant.description,
                        'cuisine_type': restaurant.cuisine_type,
                        'image': restaurant.image,
                        'rating': float(restaurant.rating or 0),
                        'total_ratings': restaurant.total_ratings or 0,
                        'avg_delivery_time': restaurant.avg_delivery_time,
                        'delivery_fee': float(restaurant.delivery_fee or 0),
                        'min_order_amount': float(restaurant.min_order_amount or 0),
                        'cost_for_two': float(restaurant.cost_for_two or 0),
                        'is_open': is_open,
                        'is_veg': restaurant.is_veg,
                        'is_pure_veg': restaurant.is_pure_veg,
                        'distance': distance,
                        'relevance_score': relevance
                    })
        
        return results
    
    def _search_dishes_fts(
        self,
        query: str,
        nearby_restaurant_ids: List[str],
        filters: Dict[str, Any],
        use_fuzzy: bool
    ) -> List[Dict[str, Any]]:
        """Search food items using FTS, fuzzy matching, and trigram prefix matching."""
        
        if not nearby_restaurant_ids:
            return []
        
        # Prepare tsquery
        tsquery = func.plainto_tsquery('english', query)
        
        # Base query with FTS ranking
        base_query = self.db.query(
            FoodItem,
            func.ts_rank(FoodItem.search_vector, tsquery).label('fts_rank'),
            func.similarity(FoodItem.name, query).label('name_similarity'),
            func.similarity(FoodItem.description, query).label('desc_similarity')
        ).filter(
            FoodItem.restaurant_id.in_(nearby_restaurant_ids),
            FoodItem.status == 'available'
        )
        
        # Apply FTS + trigram matching (production-grade)
        if use_fuzzy:
            # Use lower similarity threshold (0.1) for prefix matching
            # Trigram indexes make this fast even with low threshold
            base_query = base_query.filter(
                or_(
                    FoodItem.search_vector.op('@@')(tsquery),  # Full-text search (indexed)
                    func.similarity(FoodItem.name, query) > 0.1,  # Trigram name match (indexed)
                    func.similarity(FoodItem.description, query) > 0.15,  # Trigram description (indexed)
                    func.similarity(FoodItem.ingredients, query) > 0.15  # Trigram ingredients (indexed)
                )
            )
        else:
            base_query = base_query.filter(
                FoodItem.search_vector.op('@@')(tsquery)
            )
        
        # Apply filters
        if filters.get('is_veg_only'):
            base_query = base_query.filter(FoodItem.is_veg == True)
        
        # Execute query
        dishes = base_query.all()
        
        # Get restaurant details
        restaurant_map = {
            str(r.restaurant_id): r 
            for r in self.db.query(Restaurant).filter(
                Restaurant.restaurant_id.in_(nearby_restaurant_ids)
            ).all()
        }
        
        # Build results
        results = []
        for dish, fts_rank, name_similarity in dishes:
            restaurant = restaurant_map.get(str(dish.restaurant_id))
            if restaurant:
                # Calculate relevance (weight name similarity higher for dishes)
                relevance = (fts_rank * 2.0) + (name_similarity * 3.0)
                
                results.append({
                    'type': 'dish',
                    'id': str(dish.food_item_id),
                    'name': dish.name,
                    'description': dish.description,
                    'price': float(dish.price),
                    'discount_price': float(dish.discount_price) if dish.discount_price else None,
                    'image': dish.image,
                    'is_veg': dish.is_veg,
                    'is_popular': dish.is_popular,
                    'is_recommended': dish.is_recommended,
                    'rating': float(dish.rating or 0),
                    'total_ratings': dish.total_ratings or 0,
                    'prep_time': dish.prep_time,
                    'calories': dish.calories,
                    'restaurant_id': str(dish.restaurant_id),
                    'restaurant_name': restaurant.name,
                    'restaurant_cuisine': restaurant.cuisine_type,
                    'restaurant_rating': float(restaurant.rating or 0),
                    'restaurant_is_open': self._is_restaurant_open(restaurant),
                    'relevance_score': float(relevance)
                })
        
        return results
    
    def _search_categories_fts(
        self,
        query: str,
        use_fuzzy: bool
    ) -> List[Dict[str, Any]]:
        """Search categories using FTS and fuzzy matching."""
        
        tsquery = func.plainto_tsquery('english', query)
        
        base_query = self.db.query(
            Category,
            func.ts_rank(Category.search_vector, tsquery).label('fts_rank'),
            func.similarity(Category.name, query).label('name_similarity')
        ).filter(
            Category.is_active == True
        )
        
        if use_fuzzy:
            base_query = base_query.filter(
                or_(
                    Category.search_vector.op('@@')(tsquery),
                    func.similarity(Category.name, query) > 0.3
                )
            )
        else:
            base_query = base_query.filter(
                Category.search_vector.op('@@')(tsquery)
            )
        
        categories = base_query.all()
        
        results = []
        for category, fts_rank, name_similarity in categories:
            relevance = (fts_rank * 2.0) + (name_similarity * 3.0)
            
            results.append({
                'type': 'category',
                'id': str(category.category_id),
                'name': category.name,
                'description': category.description,
                'image': category.image,
                'relevance_score': float(relevance)
            })
        
        return results
    
    def _get_nearby_restaurant_ids(
        self,
        latitude: float,
        longitude: float,
        radius_km: float
    ) -> List[str]:
        """Get IDs of restaurants within radius."""
        
        restaurants = self.db.query(Restaurant).filter(
            Restaurant.status == 'active'
        ).all()
        
        nearby_ids = []
        for r in restaurants:
            distance = self._calculate_distance(
                latitude, longitude,
                float(r.latitude), float(r.longitude)
            )
            if distance <= radius_km:
                nearby_ids.append(str(r.restaurant_id))
        
        return nearby_ids
    
    def _calculate_distance(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float
    ) -> float:
        """Calculate distance using Haversine formula."""
        R = 6371.0  # Earth radius in km
        
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return round(R * c, 2)
    
    def _is_restaurant_open(self, restaurant: Restaurant) -> bool:
        """Check if restaurant is currently open."""
        from datetime import datetime
        
        if not restaurant.is_open:
            return False
        
        if not restaurant.opening_time or not restaurant.closing_time:
            return True
        
        current_time = datetime.now().time()
        
        if restaurant.opening_time < restaurant.closing_time:
            return restaurant.opening_time <= current_time <= restaurant.closing_time
        else:
            # Handle midnight crossover
            return current_time >= restaurant.opening_time or current_time <= restaurant.closing_time
    
    def _calculate_restaurant_relevance(
        self,
        fts_rank: float,
        name_similarity: float,
        distance: float,
        restaurant: Restaurant
    ) -> float:
        """Calculate combined relevance score for restaurants."""
        
        # Weighted scoring formula
        score = (
            (fts_rank * 3.0) +                          # FTS rank (highest weight)
            (name_similarity * 2.0) +                   # Name similarity
            (float(restaurant.rating or 0) * 0.5) +     # Rating boost
            (1.0 / (distance + 1)) * 0.3                # Distance penalty (closer = better)
        )
        
        return round(score, 4)
    
    def track_search(
        self,
        user_id: Optional[str],
        query: str,
        search_type: str,
        results_count: int,
        filters: Optional[Dict[str, Any]] = None,
        location_lat: Optional[float] = None,
        location_lng: Optional[float] = None
    ) -> None:
        """Track search in history for analytics."""
        
        try:
            search_history = SearchHistory(
                user_id=user_id,
                search_query=query,
                search_type=search_type,
                results_count=results_count,
                filters=filters,
                location_lat=location_lat,
                location_lng=location_lng
            )
            self.db.add(search_history)
            self.db.commit()
            
            # Update popular searches count
            self.db.execute(
                text("SELECT update_popular_search(:query)"),
                {"query": query}
            )
            self.db.commit()
            
        except Exception as e:
            logger.error(f"Error tracking search: {e}")
            self.db.rollback()
