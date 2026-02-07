"""
Notification API Routes

Handles all notification-related API endpoints for users and admins.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from app.infra.db.postgres.postgres_config import get_db
from app.api.dependencies import get_current_user, require_admin
from app.infra.db.postgres.models.user import User
from app.services.notification_service import NotificationService
from app.api.schemas.notification_schemas import (
    NotificationResponse,
    NotificationListResponse,
    UnreadCountResponse,
    CreateNotificationRequest,
    BroadcastNotificationRequest,
    BroadcastResponse,
    NotificationStatsResponse
)
from app.api.schemas.common_schemas import CommonResponse
from app.utils.enums import NotificationType
from app.config.logger import get_logger
import math

router = APIRouter(prefix="/notifications", tags=["notifications"])
logger = get_logger(__name__)


# ============================================
# USER NOTIFICATION ENDPOINTS
# ============================================

@router.get("", response_model=CommonResponse[NotificationListResponse])
async def get_notifications(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    unread_only: bool = Query(False, description="Show only unread notifications"),
    notification_type: Optional[NotificationType] = Query(None, description="Filter by notification type"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get paginated notifications for the current user.
    
    **Authentication:** Required
    
    **Query Parameters:**
    - `page`: Page number (default: 1)
    - `page_size`: Items per page (default: 20, max: 100)
    - `unread_only`: If true, only return unread notifications
    - `notification_type`: Filter by specific notification type
    
    **Returns:**
    - List of notifications with pagination metadata
    """
    try:
        notifications, total = NotificationService.get_user_notifications(
            db=db,
            user_id=current_user.user_id,
            page=page,
            page_size=page_size,
            unread_only=unread_only,
            notification_type=notification_type
        )
        
        # Get unread count
        unread_count = NotificationService.get_unread_count(db, current_user.user_id)
        
        # Calculate total pages
        total_pages = math.ceil(total / page_size) if total > 0 else 0
        
        # Convert to response schema
        notification_responses = [
            NotificationResponse.model_validate(notification)
            for notification in notifications
        ]
        
        response_data = NotificationListResponse(
            notifications=notification_responses,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            unread_count=unread_count
        )
        
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Notifications retrieved successfully",
            message_id="NOTIFICATIONS_RETRIEVED",
            data=response_data
        )
        
    except Exception as e:
        logger.error(f"Error fetching notifications: {e}")
        logger.error(f"Exception type: {type(e).__name__}")
        logger.error(f"Exception details: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch notifications: {str(e)}"
        )


@router.get("/unread-count", response_model=CommonResponse[UnreadCountResponse])
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get count of unread notifications for the current user.
    
    **Authentication:** Required
    
    **Returns:**
    - Count of unread notifications
    """
    try:
        unread_count = NotificationService.get_unread_count(db, current_user.user_id)
        
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Unread count retrieved successfully",
            message_id="UNREAD_COUNT_RETRIEVED",
            data=UnreadCountResponse(unread_count=unread_count)
        )
        
    except Exception as e:
        logger.error(f"Error getting unread count: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get unread count"
        )


@router.patch("/{notification_id}/read", response_model=CommonResponse[NotificationResponse])
async def mark_notification_as_read(
    notification_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark a notification as read.
    
    **Authentication:** Required
    
    **Path Parameters:**
    - `notification_id`: ID of the notification to mark as read
    
    **Returns:**
    - Updated notification
    """
    try:
        notification = NotificationService.mark_as_read(
            db=db,
            notification_id=notification_id,
            user_id=current_user.user_id
        )
        
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Notification marked as read",
            message_id="NOTIFICATION_MARKED_READ",
            data=NotificationResponse.model_validate(notification)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error marking notification as read: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to mark notification as read"
        )


@router.patch("/read-all", response_model=CommonResponse[dict])
async def mark_all_as_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark all notifications as read for the current user.
    
    **Authentication:** Required
    
    **Returns:**
    - Count of notifications marked as read
    """
    try:
        count = NotificationService.mark_all_as_read(db, current_user.user_id)
        
        return CommonResponse(
            code=status.HTTP_200_OK,
            message=f"Marked {count} notifications as read",
            message_id="ALL_NOTIFICATIONS_MARKED_READ",
            data={"count": count}
        )
        
    except Exception as e:
        logger.error(f"Error marking all notifications as read: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to mark all notifications as read"
        )


@router.delete("/{notification_id}", response_model=CommonResponse[dict])
async def delete_notification(
    notification_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a notification.
    
    **Authentication:** Required
    
    **Path Parameters:**
    - `notification_id`: ID of the notification to delete
    
    **Returns:**
    - Success message
    """
    try:
        deleted = NotificationService.delete_notification(
            db=db,
            notification_id=notification_id,
            user_id=current_user.user_id
        )
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Notification deleted successfully",
            message_id="NOTIFICATION_DELETED",
            data={"notification_id": str(notification_id)}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting notification: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete notification"
        )


# ============================================
# ADMIN NOTIFICATION ENDPOINTS
# ============================================

@router.post("/admin/send", response_model=CommonResponse[NotificationResponse])
async def create_notification(
    request: CreateNotificationRequest,
    current_admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Create a notification for a specific user (admin only).
    
    **Authentication:** Admin only
    
    **Request Body:**
    - `user_id`: User ID to send notification to
    - `title`: Notification title
    - `message`: Notification message
    - `notification_type`: Type of notification
    - `data_json`: Additional data (optional)
    
    **Returns:**
    - Created notification
    """
    try:
        notification = NotificationService.create_notification(
            db=db,
            user_id=request.user_id,
            title=request.title,
            message=request.message,
            notification_type=request.notification_type,
            data_json=request.data_json
        )
        
        return CommonResponse(
            code=status.HTTP_201_CREATED,
            message="Notification created successfully",
            message_id="NOTIFICATION_CREATED",
            data=NotificationResponse.model_validate(notification)
        )
        
    except Exception as e:
        logger.error(f"Error creating notification: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create notification"
        )


@router.post("/admin/broadcast", response_model=CommonResponse[BroadcastResponse])
async def broadcast_notification(
    request: BroadcastNotificationRequest,
    current_admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Broadcast notification to multiple users (admin only).
    
    **Authentication:** Admin only
    
    **Request Body:**
    - `title`: Notification title
    - `message`: Notification message
    - `notification_type`: Type of notification
    - `user_ids`: Specific user IDs (optional, if None sends to all users)
    - `role_filter`: Filter by user role (optional)
    - `data_json`: Additional data (optional)
    
    **Returns:**
    - Count of notifications sent and list of user IDs
    """
    try:
        count, user_ids = NotificationService.broadcast_notification(
            db=db,
            title=request.title,
            message=request.message,
            notification_type=request.notification_type,
            user_ids=request.user_ids,
            role_filter=request.role_filter,
            data_json=request.data_json
        )
        
        return CommonResponse(
            code=status.HTTP_201_CREATED,
            message=f"Broadcast sent to {count} users",
            message_id="BROADCAST_SENT",
            data=BroadcastResponse(
                message=f"Successfully sent notification to {count} users",
                notifications_sent=count,
                user_ids=user_ids
            )
        )
        
    except Exception as e:
        logger.error(f"Error broadcasting notification: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to broadcast notification"
        )


@router.get("/admin/stats", response_model=CommonResponse[NotificationStatsResponse])
async def get_notification_stats(
    current_admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Get notification statistics (admin only).
    
    **Authentication:** Admin only
    
    **Returns:**
    - Notification statistics including total, read rate, and breakdown by type
    """
    try:
        stats = NotificationService.get_notification_stats(db)
        
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Notification statistics retrieved successfully",
            message_id="NOTIFICATION_STATS_RETRIEVED",
            data=NotificationStatsResponse(
                total_notifications=stats["total_notifications"],
                total_sent_today=stats["total_sent_today"],
                total_read=stats["total_read"],
                total_unread=stats["total_unread"],
                read_rate=stats["read_rate"],
                notifications_by_type=stats["notifications_by_type"],
                recent_broadcasts=[]  # TODO: Implement recent broadcasts tracking
            )
        )
        
    except Exception as e:
        logger.error(f"Error getting notification stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get notification statistics"
        )
