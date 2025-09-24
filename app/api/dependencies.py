from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from app.infra.db.postgres.postgres_config import get_db
from app.utils.auth_utils import AuthUtils
from app.infra.db.postgres.models.user import User
from app.infra.db.postgres.models.refresh_token import RefreshToken
from app.utils.enums import UserStatus

# Security scheme
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token"""
    token = credentials.credentials
    
    # Verify JWT token
    payload = AuthUtils.verify_jwt_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    user = AuthUtils.get_user_by_id(db, payload.get("user_id"))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if user.status != UserStatus.ACTIVE.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is not active",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user (additional check for active status)"""
    if current_user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

async def get_optional_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Get current user if authenticated, otherwise return None"""
    try:
        # Try to get authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        
        token = auth_header.split(" ")[1]
        payload = AuthUtils.verify_jwt_token(token)
        if not payload:
            return None
        
        user = AuthUtils.get_user_by_id(db, payload.get("user_id"))
        if not user or user.status != UserStatus.ACTIVE:
            return None
        
        return user
    except Exception:
        return None

def get_device_info(request: Request) -> dict:
    """Extract device information from request headers"""
    return {
        "device_id": request.headers.get("x-device-id", "unknown"),
        "device_name": request.headers.get("x-device-name", "Unknown Device"),
        "device_type": request.headers.get("x-device-type", "unknown"),
        "platform": request.headers.get("x-platform", "unknown"),
        "app_version": request.headers.get("x-app-version", "1.0.0"),
        "ip_address": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent")
    }

def require_roles(*allowed_roles):
    """Dependency factory for role-based access control"""
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker

# Role-based dependencies
require_admin = require_roles("admin")
require_restaurant_owner = require_roles("restaurant_owner")
require_delivery_partner = require_roles("delivery_partner")
require_customer = require_roles("customer")
