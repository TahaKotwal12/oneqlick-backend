"""
Favorites API Routes
Handles user favorites (hearted restaurants) management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
from pydantic import BaseModel
from uuid import UUID
import logging

from app.infra.db.postgres.postgres_config import get_db
from app.api.dependencies import get_current_user
from app.infra.db.postgres.models import User, Restaurant, UserFavorite

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/favorites", tags=["Favorites"])


# ─────────────────────────────────────────────────────────────────────────────
# Response Schemas
# ─────────────────────────────────────────────────────────────────────────────

class RestaurantBrief(BaseModel):
    restaurant_id: str
    name: str
    image: Optional[str] = None
    cover_image: Optional[str] = None
    cuisine_type: Optional[str] = None
    rating: Optional[float] = None
    avg_delivery_time: Optional[int] = None
    min_order_amount: Optional[float] = None
    delivery_fee: Optional[float] = None
    is_open: bool
    is_veg: bool
    city: Optional[str] = None
    favorited_at: str

    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/")
async def get_favorites(
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get all favorited restaurants for the current user, paginated.
    """
    if page < 1:
        page = 1
    if page_size < 1 or page_size > 100:
        page_size = 20

    offset = (page - 1) * page_size

    # Join favorites with restaurants
    total_count = (
        db.query(UserFavorite)
        .filter(UserFavorite.user_id == current_user.user_id)
        .count()
    )

    rows = (
        db.query(UserFavorite, Restaurant)
        .join(Restaurant, UserFavorite.restaurant_id == Restaurant.restaurant_id)
        .filter(UserFavorite.user_id == current_user.user_id)
        .order_by(UserFavorite.created_at.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )

    favorites_list = []
    for fav, rest in rows:
        favorites_list.append({
            "restaurant_id": str(rest.restaurant_id),
            "name": rest.name,
            "image": rest.image,
            "cover_image": rest.cover_image,
            "cuisine_type": rest.cuisine_type,
            "rating": float(rest.rating) if rest.rating else None,
            "avg_delivery_time": rest.avg_delivery_time,
            "min_order_amount": float(rest.min_order_amount) if rest.min_order_amount else None,
            "delivery_fee": float(rest.delivery_fee) if rest.delivery_fee else None,
            "is_open": rest.is_open,
            "is_veg": rest.is_veg,
            "city": rest.city,
            "favorited_at": fav.created_at.isoformat() if fav.created_at else None,
        })

    return {
        "success": True,
        "data": {
            "favorites": favorites_list,
            "total_count": total_count,
            "page": page,
            "page_size": page_size,
            "has_more": (offset + page_size) < total_count,
        }
    }


@router.post("/{restaurant_id}", status_code=status.HTTP_201_CREATED)
async def add_favorite(
    restaurant_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Add a restaurant to the user's favorites.
    Returns 409 if already favorited.
    """
    # Validate restaurant exists
    restaurant = db.query(Restaurant).filter(
        Restaurant.restaurant_id == restaurant_id
    ).first()

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )

    favorite = UserFavorite(
        user_id=current_user.user_id,
        restaurant_id=restaurant_id,
    )

    try:
        db.add(favorite)
        db.commit()
        db.refresh(favorite)
        logger.info(f"User {current_user.user_id} favorited restaurant {restaurant_id}")
        return {
            "success": True,
            "message": f"Added {restaurant.name} to favorites",
            "data": {"favorite_id": str(favorite.favorite_id)},
        }
    except IntegrityError:
        db.rollback()
        # Already favorited — idempotent, just return success
        return {
            "success": True,
            "message": "Already in favorites",
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Error adding favorite: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add favorite",
        )


@router.delete("/{restaurant_id}")
async def remove_favorite(
    restaurant_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Remove a restaurant from the user's favorites.
    """
    deleted = (
        db.query(UserFavorite)
        .filter(
            UserFavorite.user_id == current_user.user_id,
            UserFavorite.restaurant_id == restaurant_id,
        )
        .delete(synchronize_session=False)
    )
    db.commit()

    if deleted == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite not found",
        )

    logger.info(f"User {current_user.user_id} removed restaurant {restaurant_id} from favorites")
    return {"success": True, "message": "Removed from favorites"}


@router.get("/check/{restaurant_id}")
async def check_favorite(
    restaurant_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Check whether a restaurant is in the current user's favorites.
    """
    exists = (
        db.query(UserFavorite)
        .filter(
            UserFavorite.user_id == current_user.user_id,
            UserFavorite.restaurant_id == restaurant_id,
        )
        .first()
    ) is not None

    return {
        "success": True,
        "data": {"is_favorite": exists, "restaurant_id": str(restaurant_id)},
    }
