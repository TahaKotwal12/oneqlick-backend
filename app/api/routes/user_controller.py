import traceback
from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session
from app.infra.db.postgres.postgres_config import get_db
from app.api.schemas.common_schemas import CommonResponse
from app.api.schemas.user_schema import (
    UserCreateRequest, UserUpdateRequest, UserResponse, UserListResponse, UserRole, UserStatus
)
from app.domain.services.user_service import UserService
from app.config.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.post("/users", 
            response_model=CommonResponse[UserResponse],
            status_code=status.HTTP_201_CREATED,
            tags=["Users"])
async def create_user(
    user_data: UserCreateRequest,
    db: Session = Depends(get_db),
):
    """
    Create a new user in the OneQlick food delivery system.
    
    This endpoint creates a new user with the provided information.
    Email and phone must be unique across the system.
    Password is securely hashed using bcrypt.
    """
    try:
        logger.info(f"Processing POST /users request for email: {user_data.email}")
        
        user_service = UserService(db)
        user = user_service.create_user(user_data)
        
        logger.info(f"Successfully created user with ID: {user.user_id}")
        return CommonResponse(
            code=status.HTTP_201_CREATED,
            message="User created successfully",
            message_id="0",
            data=UserResponse.model_validate(user)
        )
        
    except ValueError as e:
        logger.warning(f"Validation error in create_user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        error_msg = f"Error in create_user: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user"
        )

@router.get("/users/{user_id}", 
            response_model=CommonResponse[UserResponse],
            tags=["Users"])
async def get_user_by_id(
    user_id: UUID = Path(..., description="The UUID of the user to fetch"),
    db: Session = Depends(get_db),
):
    """
    Get user details by UUID.
    
    This endpoint retrieves a user's complete information from the OneQlick food delivery system.
    """
    try:
        logger.info(f"Processing GET /users/{user_id} request")
        
        user_service = UserService(db)
        user = user_service.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        logger.info(f"Successfully retrieved user data for UUID {user_id}")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="User details retrieved successfully",
            message_id="0",
            data=UserResponse.model_validate(user)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error in get_user_by_id: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching user details"
        )

@router.get("/users", 
            response_model=CommonResponse[List[UserListResponse]],
            tags=["Users"])
async def get_all_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of users to return"),
    role: Optional[UserRole] = Query(None, description="Filter by user role"),
    status_filter: Optional[UserStatus] = Query(None, alias="status", description="Filter by user status"),
    db: Session = Depends(get_db),
):
    """
    Get all users with optional filtering.
    
    This endpoint retrieves a list of users with pagination and optional filtering by role and status.
    """
    try:
        logger.info(f"Processing GET /users request with skip={skip}, limit={limit}, role={role}, status={status_filter}")
        
        user_service = UserService(db)
        users = user_service.get_all_users(
            skip=skip, 
            limit=limit, 
            role=role.value if role else None,
            status=status_filter.value if status_filter else None
        )
        
        logger.info(f"Successfully retrieved {len(users)} users")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message=f"Retrieved {len(users)} users successfully",
            message_id="0",
            data=[UserListResponse.model_validate(user) for user in users]
        )
        
    except ValueError as e:
        logger.warning(f"Validation error in get_all_users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        error_msg = f"Error in get_all_users: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching users"
        )

@router.put("/users/{user_id}", 
            response_model=CommonResponse[UserResponse],
            tags=["Users"])
async def update_user(
    user_id: UUID = Path(..., description="The UUID of the user to update"),
    update_data: UserUpdateRequest = ...,
    db: Session = Depends(get_db),
):
    """
    Update user information.
    
    This endpoint updates an existing user's information. Only provided fields will be updated.
    """
    try:
        logger.info(f"Processing PUT /users/{user_id} request")
        
        user_service = UserService(db)
        user = user_service.update_user(user_id, update_data)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        logger.info(f"Successfully updated user {user_id}")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="User updated successfully",
            message_id="0",
            data=UserResponse.model_validate(user)
        )
        
    except ValueError as e:
        logger.warning(f"Validation error in update_user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error in update_user: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the user"
        )

@router.delete("/users/{user_id}", 
               response_model=CommonResponse[dict],
               tags=["Users"])
async def delete_user(
    user_id: UUID = Path(..., description="The UUID of the user to delete"),
    db: Session = Depends(get_db),
):
    """
    Delete a user (soft delete).
    
    This endpoint performs a soft delete by setting the user status to inactive.
    """
    try:
        logger.info(f"Processing DELETE /users/{user_id} request")
        
        user_service = UserService(db)
        result = user_service.delete_user(user_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        logger.info(f"Successfully deleted user {user_id}")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="User deleted successfully",
            message_id="0",
            data={"user_id": str(user_id), "deleted": True}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error in delete_user: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the user"
        )

@router.post("/users/{user_id}/verify-email", 
             response_model=CommonResponse[dict],
             tags=["Users"])
async def verify_user_email(
    user_id: UUID = Path(..., description="The UUID of the user to verify email"),
    db: Session = Depends(get_db),
):
    """
    Mark user email as verified.
    
    This endpoint marks the user's email as verified in the system.
    """
    try:
        logger.info(f"Processing POST /users/{user_id}/verify-email request")
        
        user_service = UserService(db)
        result = user_service.verify_user_email(user_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        logger.info(f"Successfully verified email for user {user_id}")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Email verified successfully",
            message_id="0",
            data={"user_id": str(user_id), "email_verified": True}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error in verify_user_email: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while verifying email"
        )

@router.post("/users/{user_id}/verify-phone", 
             response_model=CommonResponse[dict],
             tags=["Users"])
async def verify_user_phone(
    user_id: UUID = Path(..., description="The UUID of the user to verify phone"),
    db: Session = Depends(get_db),
):
    """
    Mark user phone as verified.
    
    This endpoint marks the user's phone as verified in the system.
    """
    try:
        logger.info(f"Processing POST /users/{user_id}/verify-phone request")
        
        user_service = UserService(db)
        result = user_service.verify_user_phone(user_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        logger.info(f"Successfully verified phone for user {user_id}")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Phone verified successfully",
            message_id="0",
            data={"user_id": str(user_id), "phone_verified": True}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error in verify_user_phone: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while verifying phone"
        )