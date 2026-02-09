"""
Notification Service Layer

Handles all notification-related business logic including creation, retrieval,
marking as read, deletion, and broadcasting notifications to users.
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from typing import Optional, List
from uuid import UUID
from datetime import datetime, timezone, timedelta
from app.infra.db.postgres.models.notification import Notification
from app.infra.db.postgres.models.user import User
from app.utils.enums import NotificationType, UserRole
from app.config.logger import get_logger

logger = get_logger(__name__)


class NotificationService:
    """Service class for notification operations."""
    
    @staticmethod
    def create_notification(
        db: Session,
        user_id: UUID,
        title: str,
        message: str,
        notification_type: NotificationType,
        data_json: Optional[dict] = None
    ) -> Notification:
        """
        Create a new notification for a user.
        
        Args:
            db: Database session
            user_id: User ID to send notification to
            title: Notification title
            message: Notification message
            notification_type: Type of notification
            data_json: Additional data as JSON
            
        Returns:
            Created Notification object
        """
        try:
            notification = Notification(
                user_id=user_id,
                title=title,
                message=message,
                notification_type=notification_type,
                data_json=data_json,
                is_read=False
            )
            
            db.add(notification)
            db.commit()
            db.refresh(notification)
            
            logger.info(f"Created notification {notification.notification_id} for user {user_id}")
            
            # Send via WebSocket if user is connected
            websocket_sent = False
            try:
                from app.api.routes.websocket import manager
                import asyncio
                
                notification_dict = {
                    "notification_id": str(notification.notification_id),
                    "user_id": str(notification.user_id),
                    "title": notification.title,
                    "message": notification.message,
                    "notification_type": notification.notification_type.value,
                    "created_at": notification.created_at.isoformat(),
                    "is_read": notification.is_read,
                    "data_json": notification.data_json
                }
                
                # Check if user is connected
                if manager.is_user_connected(str(user_id)):
                    # Send notification via WebSocket (synchronous in async context)
                    try:
                        # Get or create event loop
                        try:
                            loop = asyncio.get_event_loop()
                        except RuntimeError:
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                        
                        # Run the async send_notification in the loop
                        loop.create_task(manager.send_notification(str(user_id), notification_dict))
                        logger.info(f"📬 Queued WebSocket notification for user {user_id}")
                        websocket_sent = True
                    except Exception as send_error:
                        logger.warning(f"Failed to queue WebSocket notification: {send_error}")
                else:
                    logger.debug(f"User {user_id} not connected to WebSocket, skipping real-time send")
                
            except Exception as ws_error:
                # Log WebSocket error but don't fail notification creation
                logger.warning(f"Failed to send WebSocket notification: {ws_error}")
            
            # Send push notification if WebSocket wasn't sent or as backup
            try:
                from app.services.push_notification_service import push_service
                import asyncio
                
                # Get or create event loop
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                # Send push notification asynchronously
                push_data = {
                    "notification_id": str(notification.notification_id),
                    "type": notification_type.value
                }
                if data_json:
                    push_data.update(data_json)
                
                loop.create_task(
                    push_service.send_to_user(
                        db=db,
                        user_id=str(user_id),
                        title=title,
                        message=message,
                        data=push_data
                    )
                )
                logger.info(f"📱 Queued push notification for user {user_id}")
                
            except Exception as push_error:
                logger.warning(f"Failed to send push notification: {push_error}")
            
            return notification
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating notification: {e}")
            raise
    
    @staticmethod
    def get_user_notifications(
        db: Session,
        user_id: UUID,
        page: int = 1,
        page_size: int = 20,
        unread_only: bool = False,
        notification_type: Optional[NotificationType] = None
    ) -> tuple[List[Notification], int]:
        """
        Get paginated notifications for a user.
        
        Args:
            db: Database session
            user_id: User ID
            page: Page number (1-indexed)
            page_size: Items per page
            unread_only: If True, only return unread notifications
            notification_type: Filter by notification type
            
        Returns:
            Tuple of (notifications list, total count)
        """
        try:
            query = db.query(Notification).filter(Notification.user_id == user_id)
            
            # Apply filters
            if unread_only:
                query = query.filter(Notification.is_read == False)
            
            if notification_type:
                query = query.filter(Notification.notification_type == notification_type)
            
            # Get total count
            total = query.count()
            
            # Apply pagination and ordering
            notifications = query.order_by(desc(Notification.created_at))\
                .offset((page - 1) * page_size)\
                .limit(page_size)\
                .all()
            
            return notifications, total
            
        except Exception as e:
            logger.error(f"Error fetching notifications for user {user_id}: {e}")
            raise
    
    @staticmethod
    def get_unread_count(db: Session, user_id: UUID) -> int:
        """
        Get count of unread notifications for a user.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Count of unread notifications
        """
        try:
            count = db.query(Notification)\
                .filter(and_(
                    Notification.user_id == user_id,
                    Notification.is_read == False
                ))\
                .count()
            
            return count
            
        except Exception as e:
            logger.error(f"Error getting unread count for user {user_id}: {e}")
            raise
    
    @staticmethod
    def mark_as_read(
        db: Session,
        notification_id: UUID,
        user_id: UUID
    ) -> Optional[Notification]:
        """
        Mark a notification as read.
        
        Args:
            db: Database session
            notification_id: Notification ID
            user_id: User ID (for authorization)
            
        Returns:
            Updated Notification object or None if not found
        """
        try:
            notification = db.query(Notification)\
                .filter(and_(
                    Notification.notification_id == notification_id,
                    Notification.user_id == user_id
                ))\
                .first()
            
            if not notification:
                return None
            
            notification.is_read = True
            db.commit()
            db.refresh(notification)
            
            logger.info(f"Marked notification {notification_id} as read")
            return notification
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error marking notification as read: {e}")
            raise
    
    @staticmethod
    def mark_all_as_read(db: Session, user_id: UUID) -> int:
        """
        Mark all notifications as read for a user.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Number of notifications marked as read
        """
        try:
            count = db.query(Notification)\
                .filter(and_(
                    Notification.user_id == user_id,
                    Notification.is_read == False
                ))\
                .update({"is_read": True})
            
            db.commit()
            
            logger.info(f"Marked {count} notifications as read for user {user_id}")
            return count
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error marking all notifications as read: {e}")
            raise
    
    @staticmethod
    def delete_notification(
        db: Session,
        notification_id: UUID,
        user_id: UUID
    ) -> bool:
        """
        Delete a notification.
        
        Args:
            db: Database session
            notification_id: Notification ID
            user_id: User ID (for authorization)
            
        Returns:
            True if deleted, False if not found
        """
        try:
            notification = db.query(Notification)\
                .filter(and_(
                    Notification.notification_id == notification_id,
                    Notification.user_id == user_id
                ))\
                .first()
            
            if not notification:
                return False
            
            db.delete(notification)
            db.commit()
            
            logger.info(f"Deleted notification {notification_id}")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting notification: {e}")
            raise
    
    @staticmethod
    def broadcast_notification(
        db: Session,
        title: str,
        message: str,
        notification_type: NotificationType,
        user_ids: Optional[List[UUID]] = None,
        role_filter: Optional[str] = None,
        data_json: Optional[dict] = None
    ) -> tuple[int, List[UUID]]:
        """
        Broadcast notification to multiple users (admin only).
        
        Args:
            db: Database session
            title: Notification title
            message: Notification message
            notification_type: Type of notification
            user_ids: Specific user IDs (if None, send to all or filtered by role)
            role_filter: Filter by user role
            data_json: Additional data as JSON
            
        Returns:
            Tuple of (count of notifications sent, list of user IDs)
        """
        try:
            # Determine target users
            if user_ids:
                target_user_ids = user_ids
            else:
                # Get all users or filter by role
                query = db.query(User.user_id)
                
                if role_filter:
                    query = query.filter(User.role == role_filter)
                
                target_user_ids = [user.user_id for user in query.all()]
            
            # Create notifications for all target users
            notifications = []
            for user_id in target_user_ids:
                notification = Notification(
                    user_id=user_id,
                    title=title,
                    message=message,
                    notification_type=notification_type,
                    data_json=data_json,
                    is_read=False
                )
                notifications.append(notification)
            
            db.bulk_save_objects(notifications)
            db.commit()
            
            count = len(notifications)
            logger.info(f"Broadcast {count} notifications")
            
            return count, target_user_ids
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error broadcasting notifications: {e}")
            raise
    
    @staticmethod
    def get_notification_stats(db: Session) -> dict:
        """
        Get notification statistics (admin only).
        
        Args:
            db: Database session
            
        Returns:
            Dictionary with notification statistics
        """
        try:
            # Total notifications
            total_notifications = db.query(Notification).count()
            
            # Notifications sent today
            today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
            total_sent_today = db.query(Notification)\
                .filter(Notification.created_at >= today_start)\
                .count()
            
            # Read/unread counts
            total_read = db.query(Notification).filter(Notification.is_read == True).count()
            total_unread = db.query(Notification).filter(Notification.is_read == False).count()
            
            # Read rate
            read_rate = (total_read / total_notifications * 100) if total_notifications > 0 else 0
            
            # Notifications by type
            notifications_by_type = {}
            type_counts = db.query(
                Notification.notification_type,
                func.count(Notification.notification_id)
            ).group_by(Notification.notification_type).all()
            
            for notification_type, count in type_counts:
                notifications_by_type[notification_type.value] = count
            
            return {
                "total_notifications": total_notifications,
                "total_sent_today": total_sent_today,
                "total_read": total_read,
                "total_unread": total_unread,
                "read_rate": round(read_rate, 2),
                "notifications_by_type": notifications_by_type
            }
            
        except Exception as e:
            logger.error(f"Error getting notification stats: {e}")
            raise


# Convenience functions for common notification scenarios

def notify_order_placed(db: Session, user_id: UUID, order_id: UUID, order_number: str):
    """Send notification when order is placed."""
    return NotificationService.create_notification(
        db=db,
        user_id=user_id,
        title="Order Placed Successfully",
        message=f"Your order #{order_number} has been placed successfully.",
        notification_type=NotificationType.ORDER_PLACED,
        data_json={"order_id": str(order_id), "order_number": order_number}
    )


def notify_order_confirmed(db: Session, user_id: UUID, order_id: UUID, order_number: str):
    """Send notification when order is confirmed."""
    return NotificationService.create_notification(
        db=db,
        user_id=user_id,
        title="Order Confirmed",
        message=f"Your order #{order_number} has been confirmed and is being prepared.",
        notification_type=NotificationType.ORDER_CONFIRMED,
        data_json={"order_id": str(order_id), "order_number": order_number}
    )


def notify_order_delivered(db: Session, user_id: UUID, order_id: UUID, order_number: str):
    """Send notification when order is delivered."""
    return NotificationService.create_notification(
        db=db,
        user_id=user_id,
        title="Order Delivered",
        message=f"Your order #{order_number} has been delivered. Enjoy your meal!",
        notification_type=NotificationType.ORDER_DELIVERED,
        data_json={"order_id": str(order_id), "order_number": order_number}
    )


def notify_payment_success(db: Session, user_id: UUID, order_id: UUID, amount: float):
    """Send notification when payment is successful."""
    return NotificationService.create_notification(
        db=db,
        user_id=user_id,
        title="Payment Successful",
        message=f"Payment of ₹{amount:.2f} received successfully.",
        notification_type=NotificationType.PAYMENT_SUCCESS,
        data_json={"order_id": str(order_id), "amount": amount}
    )
