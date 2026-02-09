"""
Push Notification Service for sending Expo push notifications
"""
import logging
from typing import List, Dict, Any, Optional
import requests
from datetime import datetime
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send"

class PushNotificationService:
    """Service for sending push notifications via Expo"""
    
    @staticmethod
    async def send_push_notification(
        push_tokens: List[str],
        title: str,
        message: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send push notification to multiple devices
        
        Args:
            push_tokens: List of Expo push tokens
            title: Notification title
            message: Notification body
            data: Optional data payload
            
        Returns:
            Response from Expo push service
        """
        if not push_tokens:
            logger.warning("No push tokens provided")
            return {"success": False, "error": "No tokens"}
        
        # Prepare notification payload
        messages = []
        for token in push_tokens:
            messages.append({
                "to": token,
                "sound": "default",
                "title": title,
                "body": message,
                "data": data or {},
                "priority": "high",
                "channelId": "default",
            })
        
        try:
            # Send to Expo push service
            response = requests.post(
                EXPO_PUSH_URL,
                json=messages,
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                }
            )
            
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"📱 Sent push notification to {len(push_tokens)} devices")
            logger.debug(f"Expo response: {result}")
            
            return {
                "success": True,
                "data": result,
                "sent_count": len(push_tokens)
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error sending push notification: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    async def send_to_user(
        db: Session,
        user_id: str,
        title: str,
        message: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send push notification to all active devices of a user
        
        Args:
            db: Database session
            user_id: User ID
            title: Notification title
            message: Notification body
            data: Optional data payload
            
        Returns:
            Response from push service
        """
        from app.infra.db.postgres.models.user_push_token import UserPushToken
        
        # Get all active push tokens for user
        tokens = db.query(UserPushToken).filter(
            UserPushToken.user_id == user_id,
            UserPushToken.is_active == True
        ).all()
        
        if not tokens:
            logger.debug(f"No active push tokens for user {user_id}")
            return {"success": False, "error": "No active tokens"}
        
        push_tokens = [token.push_token for token in tokens]
        
        # Send notification
        result = await PushNotificationService.send_push_notification(
            push_tokens=push_tokens,
            title=title,
            message=message,
            data=data
        )
        
        # Update last_used_at for all tokens
        if result.get("success"):
            db.query(UserPushToken).filter(
                UserPushToken.user_id == user_id,
                UserPushToken.is_active == True
            ).update({"last_used_at": datetime.utcnow()})
            db.commit()
        
        return result


# Global instance
push_service = PushNotificationService()
