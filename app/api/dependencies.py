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
    import hashlib
    
    # Generate a more unique device ID based on user agent and IP
    user_agent = request.headers.get("user-agent", "")
    ip_address = request.client.host if request.client else "unknown"
    
    # Create a hash-based device ID if not provided
    device_id = request.headers.get("x-device-id")
    if not device_id or device_id == "unknown":
        # Generate a unique device ID based on user agent and IP
        device_string = f"{user_agent}_{ip_address}"
        device_id = hashlib.md5(device_string.encode()).hexdigest()[:16]
    
    # Detect platform from user agent
    platform = request.headers.get("x-platform", "unknown")
    if platform == "unknown" and user_agent:
        if "Mobile" in user_agent or "Android" in user_agent:
            platform = "mobile"
        elif "iPhone" in user_agent or "iPad" in user_agent:
            platform = "ios"
        elif "Windows" in user_agent:
            platform = "windows"
        elif "Mac" in user_agent:
            platform = "macos"
        elif "Linux" in user_agent:
            platform = "linux"
        else:
            platform = "web"
    
    # Detect device type
    device_type = request.headers.get("x-device-type", "unknown")
    if device_type == "unknown" and user_agent:
        if "Mobile" in user_agent or "Android" in user_agent or "iPhone" in user_agent:
            device_type = "mobile"
        elif "iPad" in user_agent or "Tablet" in user_agent:
            device_type = "tablet"
        else:
            device_type = "desktop"
    
    return {
        "device_id": device_id,
        "device_name": request.headers.get("x-device-name", f"Device-{device_id[:8]}"),
        "device_type": device_type,
        "platform": platform,
        "app_version": request.headers.get("x-app-version", "1.0.0"),
        "ip_address": ip_address,
        "user_agent": user_agent
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
