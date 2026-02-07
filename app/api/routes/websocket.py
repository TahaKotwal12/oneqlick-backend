from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, status
from typing import Dict
import json
import logging
from app.utils.auth_utils import AuthUtils
from app.infra.db.postgres.models.user import User
from app.infra.db.postgres.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter()


class ConnectionManager:
    """Manages WebSocket connections for users"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, user_id: str, websocket: WebSocket):
        """Accept and store WebSocket connection"""
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.info(f"✅ User {user_id} connected to WebSocket. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, user_id: str):
        """Remove WebSocket connection"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            logger.info(f"❌ User {user_id} disconnected from WebSocket. Total connections: {len(self.active_connections)}")
    
    async def send_notification(self, user_id: str, notification: dict):
        """Send notification to specific user if connected"""
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_json(notification)
                logger.info(f"📬 Sent notification to user {user_id}: {notification.get('title')}")
                return True
            except Exception as e:
                logger.error(f"❌ Error sending notification to {user_id}: {e}")
                self.disconnect(user_id)
                return False
        else:
            logger.debug(f"User {user_id} not connected to WebSocket")
            return False
    
    async def broadcast(self, message: dict, exclude_user: str = None):
        """Broadcast message to all connected users"""
        disconnected_users = []
        
        for user_id, connection in self.active_connections.items():
            if exclude_user and user_id == exclude_user:
                continue
                
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"❌ Error broadcasting to {user_id}: {e}")
                disconnected_users.append(user_id)
        
        # Clean up disconnected users
        for user_id in disconnected_users:
            self.disconnect(user_id)
    
    def get_connection_count(self) -> int:
        """Get total number of active connections"""
        return len(self.active_connections)
    
    def is_user_connected(self, user_id: str) -> bool:
        """Check if user is connected"""
        return user_id in self.active_connections


# Global connection manager instance
manager = ConnectionManager()


async def authenticate_websocket(token: str) -> User:
    """Authenticate user for WebSocket connection"""
    try:
        # Decode JWT token
        payload = AuthUtils.decode_access_token(token)
        user_id = payload.get("user_id")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Get user from database
        db = next(get_db())
        user = db.query(User).filter(User.user_id == user_id).first()
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
        
    except Exception as e:
        logger.error(f"WebSocket authentication failed: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed")


@router.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket, token: str):
    """
    WebSocket endpoint for real-time notifications
    
    Usage:
    ws://localhost:8000/api/v1/ws/notifications?token=YOUR_ACCESS_TOKEN
    """
    user = None
    user_id = None
    
    try:
        # Authenticate user
        user = await authenticate_websocket(token)
        user_id = str(user.user_id)
        
        # Connect user
        await manager.connect(user_id, websocket)
        
        # Send welcome message
        await websocket.send_json({
            "type": "connection",
            "message": "Connected to notification service",
            "user_id": user_id
        })
        
        # Keep connection alive and handle messages
        while True:
            # Receive messages from client (heartbeat, etc.)
            data = await websocket.receive_text()
            
            # Handle heartbeat
            if data == "ping":
                await websocket.send_text("pong")
                logger.debug(f"Heartbeat from user {user_id}")
            else:
                logger.debug(f"Received message from {user_id}: {data}")
                
    except WebSocketDisconnect:
        if user_id:
            manager.disconnect(user_id)
        logger.info(f"🔌 WebSocket disconnected for user {user_id}")
        
    except HTTPException as e:
        logger.error(f"❌ WebSocket authentication error: {e.detail}")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason=e.detail)
        
    except Exception as e:
        if user_id:
            manager.disconnect(user_id)
        logger.error(f"❌ WebSocket error for user {user_id}: {e}")
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR, reason="Internal server error")


@router.get("/ws/stats")
async def get_websocket_stats():
    """Get WebSocket connection statistics (admin only)"""
    return {
        "active_connections": manager.get_connection_count(),
        "status": "operational"
    }
