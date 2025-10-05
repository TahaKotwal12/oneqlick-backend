import secrets
import string
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy.orm import Session
from app.infra.db.postgres.models.pending_user import PendingUser
from app.infra.db.postgres.models.user import User
from app.utils.enums import UserRole, UserStatus


class PendingUserUtils:
    """Utilities for managing pending user registrations."""
    
    @staticmethod
    def generate_verification_token() -> str:
        """Generate a secure verification token."""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def get_verification_expiry() -> datetime:
        """Get verification token expiry time (24 hours from now)."""
        return datetime.now(timezone.utc) + timedelta(hours=24)
    
    @staticmethod
    def create_pending_user(
        db: Session,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        password_hash: str,
        role: str = UserRole.CUSTOMER.value,
        profile_image: Optional[str] = None,
        date_of_birth: Optional[datetime] = None,
        gender: Optional[str] = None
    ) -> PendingUser:
        """Create a new pending user."""
        verification_token = PendingUserUtils.generate_verification_token()
        expires_at = PendingUserUtils.get_verification_expiry()
        
        pending_user = PendingUser(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password_hash=password_hash,
            role=role,
            profile_image=profile_image,
            date_of_birth=date_of_birth,
            gender=gender,
            verification_token=verification_token,
            expires_at=expires_at,
            is_verified=False
        )
        
        db.add(pending_user)
        db.commit()
        db.refresh(pending_user)
        return pending_user
    
    @staticmethod
    def get_pending_user_by_email(db: Session, email: str) -> Optional[PendingUser]:
        """Get pending user by email."""
        return db.query(PendingUser).filter(PendingUser.email == email).first()
    
    @staticmethod
    def get_pending_user_by_phone(db: Session, phone: str) -> Optional[PendingUser]:
        """Get pending user by phone."""
        return db.query(PendingUser).filter(PendingUser.phone == phone).first()
    
    @staticmethod
    def get_pending_user_by_token(db: Session, verification_token: str) -> Optional[PendingUser]:
        """Get pending user by verification token."""
        return db.query(PendingUser).filter(
            PendingUser.verification_token == verification_token,
            PendingUser.is_verified == False
        ).first()
    
    @staticmethod
    def is_token_expired(pending_user: PendingUser) -> bool:
        """Check if verification token is expired."""
        now = datetime.now(timezone.utc)
        expires_at = pending_user.expires_at
        
        # Ensure expires_at is timezone-aware
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        
        return now > expires_at
    
    @staticmethod
    def verify_pending_user(db: Session, verification_token: str) -> Optional[User]:
        """Verify pending user and move to main users table."""
        pending_user = PendingUserUtils.get_pending_user_by_token(db, verification_token)
        
        if not pending_user:
            return None
        
        if PendingUserUtils.is_token_expired(pending_user):
            return None
        
        # Create user in main table
        user = User(
            first_name=pending_user.first_name,
            last_name=pending_user.last_name,
            email=pending_user.email,
            phone=pending_user.phone,
            password_hash=pending_user.password_hash,
            role=pending_user.role,
            status=UserStatus.ACTIVE.value,
            profile_image=pending_user.profile_image,
            email_verified=True,  # Set as verified since they completed verification
            phone_verified=False,  # Phone verification is separate
            date_of_birth=pending_user.date_of_birth,
            gender=pending_user.gender,
            loyalty_points=0
        )
        
        db.add(user)
        
        # Mark pending user as verified
        pending_user.is_verified = True
        pending_user.updated_at = datetime.now(timezone.utc)
        
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def cleanup_expired_pending_users(db: Session) -> int:
        """Clean up expired pending users (run as a scheduled task)."""
        expired_users = db.query(PendingUser).filter(
            PendingUser.expires_at < datetime.now(timezone.utc),
            PendingUser.is_verified == False
        ).all()
        
        count = len(expired_users)
        for user in expired_users:
            db.delete(user)
        
        db.commit()
        return count
    
    @staticmethod
    def delete_pending_user(db: Session, pending_user_id: str) -> bool:
        """Delete a pending user."""
        pending_user = db.query(PendingUser).filter(
            PendingUser.pending_user_id == pending_user_id
        ).first()
        
        if pending_user:
            db.delete(pending_user)
            db.commit()
            return True
        return False
