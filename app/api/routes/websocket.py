from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, status
from typing import Dict
import json
import logging
from app.utils.auth_utils import AuthUtils
from app.infra.db.postgres.models.user import User
from app.infra.db.postgres.postgres_config import get_db

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
    user_id = None
    
    try:
        # Accept WebSocket connection first
        await websocket.accept()
        
        # Then authenticate
        try:
            payload = AuthUtils.verify_jwt_token(token)
            
            if not payload:
                await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid or expired token")
                return
                
            user_id_from_token = payload.get("user_id")
            
            if not user_id_from_token:
                await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid token")
                return
            
            # Get user from database
            db = next(get_db())
            user = db.query(User).filter(User.user_id == user_id_from_token).first()
            
            if not user:
                await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="User not found")
                return
                
            user_id = str(user.user_id)
            
        except Exception as e:
            logger.error(f"❌ WebSocket authentication failed: {e}")
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Authentication failed")
            return
        
        # Close any existing connection for this user before adding new one
        if user_id in manager.active_connections:
            try:
                old_websocket = manager.active_connections[user_id]
                logger.info(f"🔄 Closing old WebSocket connection for user {user_id}")
                await old_websocket.close(code=status.WS_1000_NORMAL_CLOSURE, reason="New connection established")
            except Exception as e:
                logger.debug(f"Error closing old connection: {e}")
        
        # Add to connection manager
        manager.active_connections[user_id] = websocket
        logger.info(f"✅ User {user_id} connected to WebSocket. Total connections: {len(manager.active_connections)}")
        
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
                logger.debug(f"💓 Heartbeat from user {user_id}")
            else:
                logger.debug(f"Received message from {user_id}: {data}")
                
    except WebSocketDisconnect:
        # Only disconnect if this is still the active connection
        if user_id and manager.active_connections.get(user_id) == websocket:
            manager.disconnect(user_id)
            logger.info(f"🔌 WebSocket disconnected for user {user_id}")
        else:
            logger.debug(f"🔌 Old WebSocket connection closed for user {user_id} (replaced by new connection)")
        
    except Exception as e:
        # Only disconnect if this is still the active connection
        if user_id and manager.active_connections.get(user_id) == websocket:
            manager.disconnect(user_id)
            logger.error(f"❌ WebSocket error for user {user_id}: {e}")
        else:
            logger.debug(f"❌ Old WebSocket connection error for user {user_id}: {e}")
        try:
            await websocket.close(code=status.WS_1011_INTERNAL_ERROR, reason="Internal server error")
        except:
            pass


@router.get("/ws/stats")
async def get_websocket_stats():
    """Get WebSocket connection statistics (admin only)"""
    return {
        "active_connections": manager.get_connection_count(),
        "status": "operational"
    }
