from jose import jwt
import bcrypt
import secrets
import string
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.config.config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_HOURS
from app.infra.db.postgres.models.user import User
from app.infra.db.postgres.models.refresh_token import RefreshToken
from app.infra.db.postgres.models.oauth_provider import OAuthProvider
from app.infra.db.postgres.models.user_session import UserSession
from app.utils.enums import UserRole, UserStatus
import httpx
import json

class AuthUtils:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    @staticmethod
    def generate_jwt_token(user_id: str, role: str, expires_delta: Optional[timedelta] = None) -> str:
        """Generate a JWT access token"""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
        
        payload = {
            "user_id": str(user_id),
            "role": role,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        }
        
        return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    
    @staticmethod
    def generate_refresh_token() -> str:
        """Generate a secure refresh token"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def verify_jwt_token(token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def generate_otp(length: int = 6) -> str:
        """Generate a numeric OTP"""
        return ''.join(secrets.choice(string.digits) for _ in range(length))
    
    @staticmethod
    async def verify_google_token(id_token: str) -> Optional[Dict[str, Any]]:
        """Verify Google ID token and return user info"""
        try:
            from app.config.config import GOOGLE_OAUTH_CONFIG
            
            # Verify the token with Google
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
                )
                
                if response.status_code == 200:
                    token_info = response.json()
                    
                    # Verify the token is for our app
                    if token_info.get("aud") == GOOGLE_OAUTH_CONFIG["client_id"]:
                        return {
                            "google_id": token_info.get("sub"),
                            "email": token_info.get("email"),
                            "name": token_info.get("name"),
                            "given_name": token_info.get("given_name"),
                            "family_name": token_info.get("family_name"),
                            "picture": token_info.get("picture"),
                            "email_verified": token_info.get("email_verified", False)
                        }
            
            return None
        except Exception as e:
            print(f"Error verifying Google token: {e}")
            return None
    
    @staticmethod
    def hash_refresh_token(token: str) -> str:
        """Hash a refresh token for database storage"""
        return bcrypt.hashpw(token.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def create_user_session(
        db: Session, 
        user_id: str, 
        device_info: Dict[str, Any],
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> UserSession:
        """Create or update a user session"""
        device_id = device_info.get("device_id", "unknown")
        
        # Check if session already exists for this user and device
        existing_session = db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.device_id == device_id,
            UserSession.is_active == True
        ).first()
        
        if existing_session:
            # Update existing session
            existing_session.device_name = device_info.get("device_name", existing_session.device_name)
            existing_session.device_type = device_info.get("device_type", existing_session.device_type)
            existing_session.platform = device_info.get("platform", existing_session.platform)
            existing_session.app_version = device_info.get("app_version", existing_session.app_version)
            existing_session.last_activity = datetime.utcnow()
            existing_session.is_active = True
            
            db.commit()
            db.refresh(existing_session)
            return existing_session
        else:
            # Create new session
            session = UserSession(
                user_id=user_id,
                device_id=device_id,
                device_name=device_info.get("device_name", "Unknown Device"),
                device_type=device_info.get("device_type", "unknown"),
                platform=device_info.get("platform", "unknown"),
                app_version=device_info.get("app_version", "1.0.0"),
                last_activity=datetime.utcnow()
            )
            
            db.add(session)
            db.commit()
            db.refresh(session)
            return session
    
    @staticmethod
    def create_refresh_token(
        db: Session,
        user_id: str,
        device_info: Dict[str, Any],
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> RefreshToken:
        """Create a new refresh token"""
        token = AuthUtils.generate_refresh_token()
        token_hash = AuthUtils.hash_password(token)
        expires_at = datetime.utcnow() + timedelta(days=30)  # 30 days
        
        refresh_token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            device_info=device_info,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        db.add(refresh_token)
        db.commit()
        db.refresh(refresh_token)
        return refresh_token
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_phone(db: Session, phone: str) -> Optional[User]:
        """Get user by phone"""
        return db.query(User).filter(User.phone == phone).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.user_id == user_id).first()
    
    @staticmethod
    def create_user(
        db: Session,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        password: str,
        role: str = UserRole.CUSTOMER.value
    ) -> User:
        """Create a new user"""
        hashed_password = AuthUtils.hash_password(password)
        
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password_hash=hashed_password,
            role=role,
            status=UserStatus.ACTIVE.value
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def create_oauth_provider(
        db: Session,
        user_id: str,
        provider: str,
        provider_user_id: str,
        provider_email: str,
        provider_name: str,
        provider_photo_url: Optional[str] = None
    ) -> OAuthProvider:
        """Create OAuth provider record"""
        oauth_provider = OAuthProvider(
            user_id=user_id,
            provider=provider,
            provider_user_id=provider_user_id,
            provider_email=provider_email,
            provider_name=provider_name,
            provider_photo_url=provider_photo_url
        )
        
        db.add(oauth_provider)
        db.commit()
        db.refresh(oauth_provider)
        return oauth_provider
