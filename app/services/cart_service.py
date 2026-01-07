"""
Cart Service
Business logic for cart operations
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from uuid import UUID, uuid4
from decimal import Decimal
from datetime import datetime, timezone
from fastapi import HTTPException, status
from typing import Optional, List

from app.infra.db.postgres.models.cart import Cart
from app.infra.db.postgres.models.cart_item import CartItem
from app.infra.db.postgres.models.food_item import FoodItem
from app.infra.db.postgres.models.food_variant import FoodVariant
from app.infra.db.postgres.models.restaurant import Restaurant
from app.api.schemas.cart_schemas import (
    AddCartItemRequest,
    UpdateCartItemRequest,
    CartResponse,
    CartItemResponse,
    RestaurantBasicInfo,
    CartSummaryResponse
)
import logging

logger = logging.getLogger(__name__)


class CartService:
    """Service class for cart operations"""
    
    @staticmethod
    def get_or_create_cart(db: Session, user_id: UUID, restaurant_id: UUID) -> Cart:
        """
        Get user's active cart or create new one.
        If cart exists for different restaurant, clear it first.
        """
        # Check if user has an active cart
        existing_cart = db.query(Cart).filter(
            Cart.user_id == user_id
        ).first()
        
        if existing_cart:
            # If cart is for different restaurant, clear it
            if existing_cart.restaurant_id != restaurant_id:
                logger.info(f"Clearing cart {existing_cart.cart_id} - different restaurant")
                # Delete all cart items
                db.query(CartItem).filter(
                    CartItem.cart_id == existing_cart.cart_id
                ).delete()
                # Update restaurant
                existing_cart.restaurant_id = restaurant_id
                existing_cart.updated_at = datetime.now(timezone.utc)
                db.commit()
                db.refresh(existing_cart)
            return existing_cart
        
        # Create new cart
        new_cart = Cart(
            cart_id=uuid4(),
            user_id=user_id,
            restaurant_id=restaurant_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        db.add(new_cart)
        db.commit()
        db.refresh(new_cart)
        
        logger.info(f"Created new cart {new_cart.cart_id} for user {user_id}")
        return new_cart
    
    @staticmethod
    def add_item_to_cart(
        db: Session,
        cart_id: UUID,
        request: AddCartItemRequest
    ) -> CartItem:
        """Add item to cart or update quantity if already exists"""
        
        # Validate food item exists and is available
        food_item = db.query(FoodItem).filter(
            FoodItem.food_item_id == request.food_item_id
        ).first()
        
        if not food_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Food item not found"
            )
        
        
        if food_item.status != 'available':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{food_item.name} is currently unavailable"
            )
        
        # Validate variant if provided
        variant = None
        variant_price = Decimal('0.00')
        if request.variant_id:
            variant = db.query(FoodVariant).filter(
                FoodVariant.food_variant_id == request.variant_id,
                FoodVariant.food_item_id == request.food_item_id
            ).first()
            
            if not variant:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Variant not found"
                )
            
            if not variant.is_available:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Variant {variant.name} is currently unavailable"
                )
            
            variant_price = variant.price_adjustment
        
        # Calculate unit price
        unit_price = food_item.price + variant_price
        total_price = unit_price * request.quantity
        
        # Check if item already exists in cart
        existing_item = db.query(CartItem).filter(
            and_(
                CartItem.cart_id == cart_id,
                CartItem.food_item_id == request.food_item_id,
                CartItem.variant_id == request.variant_id
            )
        ).first()
        
        if existing_item:
            # Update quantity
            existing_item.quantity += request.quantity
            existing_item.total_price = unit_price * existing_item.quantity
            existing_item.special_instructions = request.special_instructions
            db.commit()
            db.refresh(existing_item)
            logger.info(f"Updated cart item {existing_item.cart_item_id} quantity to {existing_item.quantity}")
            return existing_item
        
        # Create new cart item
        cart_item = CartItem(
            cart_item_id=uuid4(),
            cart_id=cart_id,
            food_item_id=request.food_item_id,
            variant_id=request.variant_id,
            quantity=request.quantity,
            unit_price=unit_price,
            total_price=total_price,
            special_instructions=request.special_instructions,
            created_at=datetime.now(timezone.utc)
        )
        
        db.add(cart_item)
        
        # Update cart timestamp
        cart = db.query(Cart).filter(Cart.cart_id == cart_id).first()
        if cart:
            cart.updated_at = datetime.now(timezone.utc)
        
        db.commit()
        db.refresh(cart_item)
        
        logger.info(f"Added new item {cart_item.cart_item_id} to cart {cart_id}")
        return cart_item
    
    @staticmethod
    def update_cart_item(
        db: Session,
        cart_item_id: UUID,
        quantity: int
    ) -> Optional[CartItem]:
        """Update cart item quantity. If quantity is 0, remove item."""
        
        cart_item = db.query(CartItem).filter(
            CartItem.cart_item_id == cart_item_id
        ).first()
        
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )
        
        if quantity == 0:
            # Remove item
            cart_id = cart_item.cart_id
            db.delete(cart_item)
            
            # Update cart timestamp
            cart = db.query(Cart).filter(Cart.cart_id == cart_id).first()
            if cart:
                cart.updated_at = datetime.now(timezone.utc)
            
            db.commit()
            logger.info(f"Removed cart item {cart_item_id}")
            return None
        
        # Update quantity and total
        cart_item.quantity = quantity
        cart_item.total_price = cart_item.unit_price * quantity
        
        # Update cart timestamp
        cart = db.query(Cart).filter(Cart.cart_id == cart_item.cart_id).first()
        if cart:
            cart.updated_at = datetime.now(timezone.utc)
        
        db.commit()
        db.refresh(cart_item)
        
        logger.info(f"Updated cart item {cart_item_id} quantity to {quantity}")
        return cart_item
    
    @staticmethod
    def remove_cart_item(db: Session, cart_item_id: UUID) -> None:
        """Remove item from cart"""
        
        cart_item = db.query(CartItem).filter(
            CartItem.cart_item_id == cart_item_id
        ).first()
        
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )
        
        cart_id = cart_item.cart_id
        db.delete(cart_item)
        
        # Update cart timestamp
        cart = db.query(Cart).filter(Cart.cart_id == cart_id).first()
        if cart:
            cart.updated_at = datetime.now(timezone.utc)
        
        db.commit()
        logger.info(f"Removed cart item {cart_item_id}")
    
    @staticmethod
    def clear_cart(db: Session, cart_id: UUID) -> None:
        """Clear all items from cart"""
        
        cart = db.query(Cart).filter(Cart.cart_id == cart_id).first()
        
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart not found"
            )
        
        # Delete all cart items
        deleted_count = db.query(CartItem).filter(
            CartItem.cart_id == cart_id
        ).delete()
        
        # Update cart timestamp
        cart.updated_at = datetime.now(timezone.utc)
        
        db.commit()
        logger.info(f"Cleared {deleted_count} items from cart {cart_id}")
    
    @staticmethod
    def get_cart(db: Session, user_id: UUID) -> Optional[Cart]:
        """Get user's active cart"""
        
        cart = db.query(Cart).filter(
            Cart.user_id == user_id
        ).first()
        
        return cart
    
    @staticmethod
    def build_cart_response(db: Session, cart: Cart) -> CartResponse:
        """Build complete cart response with items and totals"""
        
        # Get cart items with food item details
        cart_items = db.query(CartItem).filter(
            CartItem.cart_id == cart.cart_id
        ).all()
        
        # Get restaurant info
        restaurant = db.query(Restaurant).filter(
            Restaurant.restaurant_id == cart.restaurant_id
        ).first()
        
        # Build cart item responses
        item_responses = []
        subtotal = Decimal('0.00')
        
        for cart_item in cart_items:
            food_item = db.query(FoodItem).filter(
                FoodItem.food_item_id == cart_item.food_item_id
            ).first()
            
            variant = None
            variant_name = None
            if cart_item.variant_id:
                variant = db.query(FoodVariant).filter(
                    FoodVariant.food_variant_id == cart_item.variant_id
                ).first()
                variant_name = variant.name if variant else None
            
            item_response = CartItemResponse(
                cart_item_id=cart_item.cart_item_id,
                food_item_id=cart_item.food_item_id,
                food_item_name=food_item.name if food_item else "Unknown",
                food_item_image=food_item.image if food_item else None,
                variant_id=cart_item.variant_id,
                variant_name=variant_name,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                total_price=cart_item.total_price,
                special_instructions=cart_item.special_instructions,
                is_veg=food_item.is_veg if food_item else True,
                is_available=food_item.is_available if food_item else False
            )
            
            item_responses.append(item_response)
            subtotal += cart_item.total_price
        
        # Build restaurant info
        restaurant_info = RestaurantBasicInfo(
            restaurant_id=restaurant.restaurant_id,
            name=restaurant.name,
            image=restaurant.image,
            address_line1=restaurant.address_line1,
            city=restaurant.city
        ) if restaurant else None
        
        # Build cart response
        cart_response = CartResponse(
            cart_id=cart.cart_id,
            user_id=cart.user_id,
            restaurant_id=cart.restaurant_id,
            restaurant=restaurant_info,
            items=item_responses,
            item_count=len(item_responses),
            subtotal=subtotal,
            created_at=cart.created_at,
            updated_at=cart.updated_at
        )
        
        return cart_response
    
    @staticmethod
    def get_cart_summary(db: Session, cart: Cart) -> CartSummaryResponse:
        """Get quick cart summary"""
        
        # Get cart items count and subtotal
        cart_items = db.query(CartItem).filter(
            CartItem.cart_id == cart.cart_id
        ).all()
        
        item_count = len(cart_items)
        subtotal = sum(item.total_price for item in cart_items)
        
        # Get restaurant name
        restaurant = db.query(Restaurant).filter(
            Restaurant.restaurant_id == cart.restaurant_id
        ).first()
        
        return CartSummaryResponse(
            cart_id=cart.cart_id,
            item_count=item_count,
            subtotal=subtotal,
            restaurant_name=restaurant.name if restaurant else "Unknown"
        )
