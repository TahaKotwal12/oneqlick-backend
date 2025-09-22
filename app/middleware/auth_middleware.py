import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from app.infra.db.postgres.postgres_config import get_db
from app.infra.db.postgres.models.user import User
from app.api.schemas.auth_schemas import TokenData
from app.config.config import JWT_SECRET_KEY, JWT_ALGORITHM
from app.config.logger import get_logger

logger = get_logger(__name__)

# HTTP Bearer token scheme
security = HTTPBearer()

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """
    Verify JWT token and extract user information.
    
    Args:
        credentials: HTTP Bearer token from request header
        
    Returns:
        TokenData: Decoded token information
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        token = credentials.credentials
        
        # Decode JWT token
        payload = jwt.decode(
            token, 
            JWT_SECRET_KEY, 
            algorithms=[JWT_ALGORITHM]
        )
        
        # Validate token type
        if payload.get('type') != 'access':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        # Extract user information
        user_id = payload.get('user_id')
        email = payload.get('email')
        role = payload.get('role')
        session_id = payload.get('session_id')
        
        if not user_id or not email or not role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        return TokenData(
            user_id=user_id,
            email=email,
            role=role,
            session_id=session_id
        )
        
    except jwt.ExpiredSignatureError:
        logger.warning("JWT token expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        logger.warning("Invalid JWT token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except Exception as e:
        logger.error(f"JWT verification error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token verification failed"
        )

def get_current_user(
    token_data: TokenData = Depends(verify_jwt_token),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from database.
    
    Args:
        token_data: Decoded JWT token data
        db: Database session
        
    Returns:
        User: Current authenticated user
        
    Raises:
        HTTPException: If user not found or inactive
    """
    try:
        # Get user from database
        user = db.query(User).filter(User.user_id == token_data.user_id).first()
        
        if not user:
            logger.warning(f"User not found: {token_data.user_id}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        # Check if user is active
        if user.status.value != 'active':
            logger.warning(f"Inactive user attempted access: {token_data.user_id}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is inactive"
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get current user error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user information"
        )

def require_role(required_roles: list[str]):
    """
    Decorator to require specific user roles.
    
    Args:
        required_roles: List of allowed roles
        
    Returns:
        Decorator function
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role.value not in required_roles:
            logger.warning(f"User {current_user.user_id} with role {current_user.role.value} attempted to access restricted resource")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    
    return role_checker

def require_customer(current_user: User = Depends(get_current_user)) -> User:
    """Require customer role."""
    return require_role(['customer'])(current_user)

def require_restaurant_owner(current_user: User = Depends(get_current_user)) -> User:
    """Require restaurant owner role."""
    return require_role(['restaurant_owner'])(current_user)

def require_delivery_partner(current_user: User = Depends(get_current_user)) -> User:
    """Require delivery partner role."""
    return require_role(['delivery_partner'])(current_user)

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Require admin role."""
    return require_role(['admin'])(current_user)

def require_any_role(current_user: User = Depends(get_current_user)) -> User:
    """Allow any authenticated user."""
    return current_user
