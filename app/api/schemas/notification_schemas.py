from pydantic import BaseModel, Field, UUID4
from typing import Optional, List
from datetime import datetime
from app.utils.enums import NotificationType


# ============================================
# Request Schemas
# ============================================

class CreateNotificationRequest(BaseModel):
    """Request schema for creating a notification (admin only)."""
    user_id: UUID4 = Field(..., description="User ID to send notification to")
    title: str = Field(..., min_length=1, max_length=255, description="Notification title")
    message: str = Field(..., min_length=1, description="Notification message")
    notification_type: NotificationType = Field(..., description="Type of notification")
    data_json: Optional[dict] = Field(None, description="Additional data as JSON")


class BroadcastNotificationRequest(BaseModel):
    """Request schema for broadcasting notification to multiple users (admin only)."""
    title: str = Field(..., min_length=1, max_length=255, description="Notification title")
    message: str = Field(..., min_length=1, description="Notification message")
    notification_type: NotificationType = Field(..., description="Type of notification")
    user_ids: Optional[List[UUID4]] = Field(None, description="Specific user IDs (if None, send to all)")
    role_filter: Optional[str] = Field(None, description="Filter by user role (customer, admin, etc.)")
    data_json: Optional[dict] = Field(None, description="Additional data as JSON")


class RegisterPushTokenRequest(BaseModel):
    """Request schema for registering a push token."""
    push_token: str = Field(..., description="Expo push token")
    device_type: str = Field(..., pattern="^(ios|android)$", description="Device platform ('ios' or 'android')")


class MarkAsReadRequest(BaseModel):
    """Request schema for marking notification as read."""
    notification_id: UUID4 = Field(..., description="Notification ID to mark as read")


# ============================================
# Response Schemas
# ============================================

class NotificationResponse(BaseModel):
    """Response schema for a single notification."""
    notification_id: UUID4
    user_id: UUID4
    title: str
    message: str
    notification_type: NotificationType
    is_read: bool
    data_json: Optional[dict]
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):
    """Response schema for paginated notification list."""
    notifications: List[NotificationResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    unread_count: int


class UnreadCountResponse(BaseModel):
    """Response schema for unread notification count."""
    unread_count: int


class NotificationStatsResponse(BaseModel):
    """Response schema for notification statistics (admin only)."""
    total_notifications: int
    total_sent_today: int
    total_read: int
    total_unread: int
    read_rate: float
    notifications_by_type: dict
    recent_broadcasts: List[dict]


class BroadcastResponse(BaseModel):
    """Response schema for broadcast notification."""
    message: str
    notifications_sent: int
    user_ids: List[UUID4]
