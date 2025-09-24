from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone

from app.infra.db.postgres.postgres_config import get_db
from app.api.dependencies import get_current_user, require_admin, require_customer
from app.api.schemas.user_schemas import (
    UserUpdateRequest, PasswordChangeRequest, AddressCreateRequest, AddressUpdateRequest,
    UserPreferencesRequest, UserResponse, UserProfileResponse, UserStatsResponse,
    UserSessionResponse, UserSessionsResponse, UserListResponse, UserSearchRequest,
    UserStatusUpdateRequest, UserRoleUpdateRequest, PaginationParams, AddressResponse
)
from app.api.schemas.common_schemas import CommonResponse
from app.infra.db.postgres.models.user import User
from app.infra.db.postgres.models.address import Address
from app.infra.db.postgres.models.user_session import UserSession
from app.infra.db.postgres.models.order import Order
from app.utils.auth_utils import AuthUtils
from app.utils.enums import UserRole, UserStatus
from app.config.logger import get_logger

router = APIRouter(prefix="/users", tags=["users"])
logger = get_logger(__name__)

# Constants
USER_NOT_FOUND_MESSAGE = "User not found"

# User Profile Management
@router.get("/profile", response_model=CommonResponse[UserProfileResponse])
async def get_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's profile with addresses"""
    try:
        # Get user addresses
        addresses = db.query(Address).filter(
            Address.user_id == current_user.user_id
        ).all()
        
        # Get user preferences (placeholder - you can implement this later)
        preferences = {
            "email_notifications": True,
            "sms_notifications": True,
            "push_notifications": True,
            "marketing_emails": False,
            "language": "en",
            "currency": "USD"
        }
        
        profile_data = UserProfileResponse(
            user=current_user,
            addresses=addresses,
            preferences=preferences
        )
        
        return CommonResponse(
            code=200,
            message="User profile retrieved successfully",
            message_id="USER_PROFILE_SUCCESS",
            data=profile_data
        )
    
    except Exception as e:
        logger.error(f"Error getting user profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user profile"
        )

@router.put("/profile", response_model=CommonResponse[UserResponse])
async def update_user_profile(
    profile_data: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile"""
    try:
        # Check if email is being changed and if it's already taken
        if profile_data.email and profile_data.email != current_user.email:
            existing_user = AuthUtils.get_user_by_email(db, profile_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )
        
        # Check if phone is being changed and if it's already taken
        if profile_data.phone and profile_data.phone != current_user.phone:
            existing_user = AuthUtils.get_user_by_phone(db, profile_data.phone)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Phone number already exists"
                )
        
        # Update user fields
        update_data = profile_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            # Special handling for gender field to ensure proper enum value
            if field == 'gender' and value is not None:
                # Convert to proper enum value
                if isinstance(value, str):
                    value = value.lower()
                # Map to enum
                gender_map = {'male': Gender.MALE, 'female': Gender.FEMALE, 'other': Gender.OTHER}
                if value in gender_map:
                    setattr(current_user, field, gender_map[value])
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid gender value"
                    )
            else:
                setattr(current_user, field, value)
        
        current_user.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(current_user)
        
        return CommonResponse(
            code=200,
            message="Profile updated successfully",
            message_id="PROFILE_UPDATE_SUCCESS",
            data=current_user
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )

@router.put("/password", response_model=CommonResponse[dict])
async def change_password(
    password_data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    try:
        # Verify current password
        if not AuthUtils.verify_password(password_data.current_password, current_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Update password
        current_user.password_hash = AuthUtils.hash_password(password_data.new_password)
        current_user.updated_at = datetime.now(timezone.utc)
        db.commit()
        
        return CommonResponse(
            code=200,
            message="Password changed successfully",
            message_id="PASSWORD_CHANGE_SUCCESS",
            data={"message": "Password updated successfully"}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error changing password: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change password"
        )

@router.get("/stats", response_model=CommonResponse[UserStatsResponse])
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user statistics"""
    try:
        # Get order statistics
        orders = db.query(Order).filter(Order.user_id == current_user.user_id).all()
        
        total_orders = len(orders)
        total_spent = sum(order.total_amount for order in orders if order.total_amount)
        
        # Get last order date
        last_order_date = None
        if orders:
            last_order = max(orders, key=lambda x: x.created_at)
            last_order_date = last_order.created_at
        
        stats = UserStatsResponse(
            total_orders=total_orders,
            total_spent=float(total_spent) if total_spent else 0.0,
            loyalty_points=current_user.loyalty_points,
            member_since=current_user.created_at,
            favorite_cuisines=[],  # Placeholder - implement cuisine tracking
            last_order_date=last_order_date
        )
        
        return CommonResponse(
            code=200,
            message="User statistics retrieved successfully",
            message_id="USER_STATS_SUCCESS",
            data=stats
        )
    
    except Exception as e:
        logger.error(f"Error getting user stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user statistics"
        )

# Address Management
@router.post("/addresses", response_model=CommonResponse[AddressResponse])
async def create_address(
    address_data: AddressCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new address for the user"""
    try:
        # If this is set as default, unset other default addresses
        if address_data.is_default:
            db.query(Address).filter(
                Address.user_id == current_user.user_id,
                Address.is_default == True
            ).update({"is_default": False})
        
        # Create new address
        address = Address(
            user_id=current_user.user_id,
            **address_data.dict()
        )
        
        db.add(address)
        db.commit()
        db.refresh(address)
        
        return CommonResponse(
            code=201,
            message="Address created successfully",
            message_id="ADDRESS_CREATE_SUCCESS",
            data=address
        )
    
    except Exception as e:
        logger.error(f"Error creating address: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create address"
        )

@router.get("/addresses", response_model=CommonResponse[List[AddressResponse]])
async def get_user_addresses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all addresses for the current user"""
    try:
        addresses = db.query(Address).filter(
            Address.user_id == current_user.user_id
        ).order_by(Address.is_default.desc(), Address.created_at.desc()).all()
        
        return CommonResponse(
            code=200,
            message="Addresses retrieved successfully",
            message_id="ADDRESSES_GET_SUCCESS",
            data=addresses
        )
    
    except Exception as e:
        logger.error(f"Error getting addresses: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve addresses"
        )

@router.put("/addresses/{address_id}", response_model=CommonResponse[AddressResponse])
async def update_address(
    address_id: UUID,
    address_data: AddressUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a specific address"""
    try:
        # Get the address
        address = db.query(Address).filter(
            Address.address_id == address_id,
            Address.user_id == current_user.user_id
        ).first()
        
        if not address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found"
            )
        
        # If setting as default, unset other default addresses
        if address_data.is_default:
            db.query(Address).filter(
                Address.user_id == current_user.user_id,
                Address.is_default == True,
                Address.address_id != address_id
            ).update({"is_default": False})
        
        # Update address fields
        update_data = address_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(address, field, value)
        
        db.commit()
        db.refresh(address)
        
        return CommonResponse(
            code=200,
            message="Address updated successfully",
            message_id="ADDRESS_UPDATE_SUCCESS",
            data=address
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating address: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update address"
        )

@router.delete("/addresses/{address_id}", response_model=CommonResponse[dict])
async def delete_address(
    address_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a specific address"""
    try:
        # Get the address
        address = db.query(Address).filter(
            Address.address_id == address_id,
            Address.user_id == current_user.user_id
        ).first()
        
        if not address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found"
            )
        
        db.delete(address)
        db.commit()
        
        return CommonResponse(
            code=200,
            message="Address deleted successfully",
            message_id="ADDRESS_DELETE_SUCCESS",
            data={"message": "Address deleted successfully"}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting address: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete address"
        )

# Session Management
@router.get("/sessions", response_model=CommonResponse[UserSessionsResponse])
async def get_user_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all active sessions for the current user"""
    try:
        sessions = db.query(UserSession).filter(
            UserSession.user_id == current_user.user_id
        ).order_by(UserSession.last_activity.desc()).all()
        
        return CommonResponse(
            code=200,
            message="User sessions retrieved successfully",
            message_id="USER_SESSIONS_SUCCESS",
            data=UserSessionsResponse(
                sessions=sessions,
                total_sessions=len(sessions)
            )
        )
    
    except Exception as e:
        logger.error(f"Error getting user sessions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user sessions"
        )

@router.delete("/sessions/{session_id}", response_model=CommonResponse[dict])
async def revoke_session(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Revoke a specific session"""
    try:
        session = db.query(UserSession).filter(
            UserSession.session_id == session_id,
            UserSession.user_id == current_user.user_id
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        session.is_active = False
        session.updated_at = datetime.now(timezone.utc)
        db.commit()
        
        return CommonResponse(
            code=200,
            message="Session revoked successfully",
            message_id="SESSION_REVOKE_SUCCESS",
            data={"message": "Session revoked successfully"}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error revoking session: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to revoke session"
        )

# Admin-only endpoints
@router.get("/admin/users", response_model=CommonResponse[UserListResponse])
async def get_all_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    role: Optional[UserRole] = Query(None),
    status: Optional[UserStatus] = Query(None),
    search: Optional[str] = Query(None),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get all users (admin only)"""
    try:
        query = db.query(User)
        
        # Apply filters
        if role:
            query = query.filter(User.role == role.value)
        if status:
            query = query.filter(User.status == status.value)
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (User.first_name.ilike(search_term)) |
                (User.last_name.ilike(search_term)) |
                (User.email.ilike(search_term)) |
                (User.phone.ilike(search_term))
            )
        
        # Get total count
        total_users = query.count()
        
        # Apply pagination
        offset = (page - 1) * page_size
        users = query.offset(offset).limit(page_size).all()
        
        total_pages = (total_users + page_size - 1) // page_size
        
        return CommonResponse(
            code=200,
            message="Users retrieved successfully",
            message_id="USERS_GET_SUCCESS",
            data=UserListResponse(
                users=users,
                total_users=total_users,
                page=page,
                page_size=page_size,
                total_pages=total_pages
            )
        )
    
    except Exception as e:
        logger.error(f"Error getting all users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve users"
        )

@router.get("/admin/users/{user_id}", response_model=CommonResponse[UserResponse])
async def get_user_by_id_admin(
    user_id: UUID,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get user by ID (admin only)"""
    try:
        user = AuthUtils.get_user_by_id(db, str(user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=USER_NOT_FOUND_MESSAGE
            )
        
        return CommonResponse(
            code=200,
            message="User retrieved successfully",
            message_id="USER_GET_SUCCESS",
            data=user
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user by ID: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user"
        )

@router.put("/admin/users/{user_id}/status", response_model=CommonResponse[UserResponse])
async def update_user_status(
    user_id: UUID,
    status_data: UserStatusUpdateRequest,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update user status (admin only)"""
    try:
        user = AuthUtils.get_user_by_id(db, str(user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=USER_NOT_FOUND_MESSAGE
            )
        
        user.status = status_data.status.value
        user.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(user)
        
        return CommonResponse(
            code=200,
            message="User status updated successfully",
            message_id="USER_STATUS_UPDATE_SUCCESS",
            data=user
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user status"
        )

@router.put("/admin/users/{user_id}/role", response_model=CommonResponse[UserResponse])
async def update_user_role(
    user_id: UUID,
    role_data: UserRoleUpdateRequest,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update user role (admin only)"""
    try:
        user = AuthUtils.get_user_by_id(db, str(user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=USER_NOT_FOUND_MESSAGE
            )
        
        user.role = role_data.role.value
        user.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(user)
        
        return CommonResponse(
            code=200,
            message="User role updated successfully",
            message_id="USER_ROLE_UPDATE_SUCCESS",
            data=user
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user role: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user role"
        )
