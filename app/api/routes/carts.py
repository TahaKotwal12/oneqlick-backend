"""
Cart API Routes
Endpoints for cart management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app.infra.db.postgres.postgres_config import get_db
from app.infra.db.postgres.models.user import User
from app.api.dependencies import get_current_user
from app.services.cart_service import CartService
from app.api.schemas.cart_schemas import (
    AddCartItemRequest,
    UpdateCartItemRequest,
    RemoveCartItemRequest,
    CartResponse,
    CartItemAddedResponse,
    CartSummaryResponse
)
from app.api.schemas.common_schemas import CommonResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/add-item", response_model=CommonResponse[CartItemAddedResponse], status_code=201)
async def add_item_to_cart(
    request: AddCartItemRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add item to cart.
    
    - Creates cart if doesn't exist
    - Clears cart if adding from different restaurant
    - Updates quantity if item already in cart
    - Returns cart summary
    """
    try:
        logger.info(f"Adding item {request.food_item_id} to cart for user {current_user.user_id}")
        
        # Get food item to determine restaurant
        from app.infra.db.postgres.models.food_item import FoodItem
        food_item = db.query(FoodItem).filter(
            FoodItem.food_item_id == request.food_item_id
        ).first()
        
        if not food_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Food item not found"
            )
        
        # Get or create cart
        cart = CartService.get_or_create_cart(
            db=db,
            user_id=current_user.user_id,
            restaurant_id=food_item.restaurant_id
        )
        
        # Add item to cart
        cart_item = CartService.add_item_to_cart(
            db=db,
            cart_id=cart.cart_id,
            request=request
        )
        
        # Get cart summary
        cart_summary = CartService.get_cart_summary(db, cart)
        
        return CommonResponse(
            success=True,
            message="Item added to cart successfully",
            data=CartItemAddedResponse(
                cart_id=cart.cart_id,
                cart_item_id=cart_item.cart_item_id,
                message="Item added to cart",
                cart_summary=cart_summary
            )
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding item to cart: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add item to cart: {str(e)}"
        )


@router.put("/update-item", response_model=CommonResponse[CartSummaryResponse])
async def update_cart_item(
    request: UpdateCartItemRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update cart item quantity.
    
    - Set quantity to 0 to remove item
    - Returns updated cart summary
    """
    try:
        logger.info(f"Updating cart item {request.cart_item_id} to quantity {request.quantity}")
        
        # Update cart item
        cart_item = CartService.update_cart_item(
            db=db,
            cart_item_id=request.cart_item_id,
            quantity=request.quantity
        )
        
        # Get user's cart
        cart = CartService.get_cart(db, current_user.user_id)
        
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart not found"
            )
        
        # Get cart summary
        cart_summary = CartService.get_cart_summary(db, cart)
        
        message = "Item removed from cart" if request.quantity == 0 else "Cart updated successfully"
        
        return CommonResponse(
            success=True,
            message=message,
            data=cart_summary
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating cart item: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update cart item: {str(e)}"
        )


@router.delete("/remove-item", response_model=CommonResponse[CartSummaryResponse])
async def remove_cart_item(
    request: RemoveCartItemRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove item from cart.
    
    - Returns updated cart summary
    """
    try:
        logger.info(f"Removing cart item {request.cart_item_id}")
        
        # Remove cart item
        CartService.remove_cart_item(
            db=db,
            cart_item_id=request.cart_item_id
        )
        
        # Get user's cart
        cart = CartService.get_cart(db, current_user.user_id)
        
        if not cart:
            # Cart might be empty now
            return CommonResponse(
                success=True,
                message="Item removed from cart",
                data=CartSummaryResponse(
                    cart_id=cart.cart_id if cart else None,
                    item_count=0,
                    subtotal=0.00,
                    restaurant_name=""
                )
            )
        
        # Get cart summary
        cart_summary = CartService.get_cart_summary(db, cart)
        
        return CommonResponse(
            success=True,
            message="Item removed from cart",
            data=cart_summary
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing cart item: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to remove cart item: {str(e)}"
        )


@router.get("", response_model=CommonResponse[CartResponse])
async def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's current cart with all items and details.
    
    - Returns complete cart information
    - Returns empty cart if no active cart
    """
    try:
        logger.info(f"Getting cart for user {current_user.user_id}")
        
        # Get user's cart
        cart = CartService.get_cart(db, current_user.user_id)
        
        if not cart:
            # Return empty cart response
            return CommonResponse(
                success=True,
                message="No active cart",
                data=None
            )
        
        # Build cart response
        cart_response = CartService.build_cart_response(db, cart)
        
        return CommonResponse(
            success=True,
            message="Cart retrieved successfully",
            data=cart_response
        )
        
    except Exception as e:
        logger.error(f"Error getting cart: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get cart: {str(e)}"
        )


@router.delete("/clear", response_model=CommonResponse[dict])
async def clear_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Clear all items from cart.
    
    - Removes all cart items
    - Keeps cart for future use
    """
    try:
        logger.info(f"Clearing cart for user {current_user.user_id}")
        
        # Get user's cart
        cart = CartService.get_cart(db, current_user.user_id)
        
        if not cart:
            return CommonResponse(
                success=True,
                message="No active cart to clear",
                data={"cart_id": None}
            )
        
        # Clear cart
        CartService.clear_cart(db, cart.cart_id)
        
        return CommonResponse(
            success=True,
            message="Cart cleared successfully",
            data={"cart_id": str(cart.cart_id)}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error clearing cart: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear cart: {str(e)}"
        )


@router.get("/summary", response_model=CommonResponse[CartSummaryResponse])
async def get_cart_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get quick cart summary (item count and total).
    
    - Lightweight endpoint for cart badge
    - Returns summary or null if no cart
    """
    try:
        logger.info(f"Getting cart summary for user {current_user.user_id}")
        
        # Get user's cart
        cart = CartService.get_cart(db, current_user.user_id)
        
        if not cart:
            return CommonResponse(
                success=True,
                message="No active cart",
                data=None
            )
        
        # Get cart summary
        cart_summary = CartService.get_cart_summary(db, cart)
        
        return CommonResponse(
            success=True,
            message="Cart summary retrieved successfully",
            data=cart_summary
        )
        
    except Exception as e:
        logger.error(f"Error getting cart summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get cart summary: {str(e)}"
        )
