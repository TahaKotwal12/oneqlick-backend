import secrets
import string
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.infra.db.postgres.models.pending_user import PendingUser
from app.infra.db.postgres.models.user import User
from app.utils.enums import UserRole, UserStatus
import logging

logger = logging.getLogger(__name__)


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
        gender: Optional[str] = None,
        restaurant_name: Optional[str] = None,
        cuisine_type: Optional[str] = None,
        vehicle_type: Optional[str] = None,
        license_number: Optional[str] = None
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
            restaurant_name=restaurant_name,
            cuisine_type=cuisine_type,
            vehicle_type=vehicle_type,
            license_number=license_number,
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
        db.flush()  # Flush to get user_id before creating restaurant/delivery partner
        
        # If restaurant owner, create restaurant from pending user data
        if pending_user.role == UserRole.RESTAURANT_OWNER.value and pending_user.restaurant_name:
            from app.infra.db.postgres.models.restaurant import Restaurant
            from datetime import time
            
            try:
                restaurant = Restaurant(
                    owner_id=user.user_id,
                    name=pending_user.restaurant_name,
                    description=f"Welcome to {pending_user.restaurant_name}!",
                    phone=user.phone,
                    email=user.email,
                    cuisine_type=pending_user.cuisine_type or 'Multi-Cuisine',
                    # Set default values for required fields
                    address_line1="Address not set",
                    city="City not set",
                    state="State not set",
                    postal_code="000000",
                    latitude=0.0,
                    longitude=0.0,
                    avg_delivery_time=30,
                    min_order_amount=100.0,
                    delivery_fee=40.0,
                    rating=0.0,
                    total_ratings=0,
                    status='active',
                    is_open=True,
                    opening_time=time(9, 0),
                    closing_time=time(22, 0),
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc)
                )
                
                db.add(restaurant)
                logger.info(f"Created restaurant '{restaurant.name}' for user {user.user_id}")
                
            except Exception as e:
                logger.error(f"Error creating restaurant for user {user.user_id}: {str(e)}")
                # Don't fail user creation if restaurant creation fails
        
        # If delivery partner, create delivery partner record
        elif pending_user.role == UserRole.DELIVERY_PARTNER.value:
            # Validate required fields
            if not pending_user.license_number:
                logger.error(f"Delivery partner signup missing license_number for user {pending_user.email}")
                raise ValueError("License number is required for delivery partners")
            
            from app.infra.db.postgres.models.delivery_partner import DeliveryPartner
            from app.utils.enums import VehicleType, AvailabilityStatus
            
            # Validate and convert vehicle_type
            vehicle_type_str = (pending_user.vehicle_type or 'motorcycle').lower().strip()
            
            # Validate against allowed values
            valid_vehicle_types = [vt.value for vt in VehicleType]
            if vehicle_type_str not in valid_vehicle_types:
                logger.error(f"Invalid vehicle_type '{vehicle_type_str}' for user {pending_user.email}. Valid types: {valid_vehicle_types}")
                raise ValueError(f"Invalid vehicle type '{vehicle_type_str}'. Must be one of: {', '.join(valid_vehicle_types)}")
            
            vehicle_type_enum = VehicleType(vehicle_type_str)
            
            logger.info(f"Creating delivery partner for user {pending_user.email}: vehicle_type={vehicle_type_enum.value}, license_number={pending_user.license_number}")
            
            delivery_partner = DeliveryPartner(
                user_id=user.user_id,
                vehicle_type=vehicle_type_enum,
                vehicle_number="PENDING",  # Clear placeholder - can be updated later
                license_number=pending_user.license_number,
                availability_status=AvailabilityStatus.OFFLINE,
                rating=0.0,
                total_ratings=0,
                total_deliveries=0,
                is_verified=False,  # Needs document verification
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            
            db.add(delivery_partner)
            logger.info(f"Successfully created delivery partner record for user {user.user_id} with vehicle type {vehicle_type_enum.value}")
        
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
    
    @staticmethod
    def check_otp_lockout_status(pending_user: PendingUser) -> Dict[str, Any]:
        """Check if a pending user is currently locked out from OTP requests."""
        now = datetime.now(timezone.utc)
        
        # Check if user is currently locked out
        if pending_user.otp_locked_until and now < pending_user.otp_locked_until:
            remaining_lockout_seconds = int((pending_user.otp_locked_until - now).total_seconds())
            return {
                "is_locked": True,
                "remaining_seconds": remaining_lockout_seconds,
                "locked_until": pending_user.otp_locked_until,
                "attempts_used": pending_user.otp_attempts,
                "max_attempts": pending_user.max_otp_attempts
            }
        
        # Check if user has exceeded attempts but lockout has expired
        if pending_user.otp_attempts >= pending_user.max_otp_attempts:
            # Reset attempts if lockout has expired
            pending_user.otp_attempts = 0
            pending_user.otp_locked_until = None
            db.commit()
        
        return {
            "is_locked": False,
            "remaining_seconds": 0,
            "locked_until": None,
            "attempts_used": pending_user.otp_attempts,
            "max_attempts": pending_user.max_otp_attempts
        }
    
    @staticmethod
    def increment_otp_attempts(db: Session, pending_user: PendingUser) -> Dict[str, Any]:
        """Increment OTP attempts for a pending user and check if lockout is needed."""
        pending_user.otp_attempts += 1
        
        # Check if user should be locked out
        if pending_user.otp_attempts >= pending_user.max_otp_attempts:
            # Lock the user for the specified duration
            lockout_duration = timedelta(minutes=pending_user.lockout_duration_minutes)
            pending_user.otp_locked_until = datetime.now(timezone.utc) + lockout_duration
            
            logger.info(f"User {pending_user.email} locked out for {pending_user.lockout_duration_minutes} minutes due to OTP limit")
        
        db.commit()
        
        return {
            "attempts_used": pending_user.otp_attempts,
            "max_attempts": pending_user.max_otp_attempts,
            "is_locked": pending_user.otp_attempts >= pending_user.max_otp_attempts,
            "locked_until": pending_user.otp_locked_until
        }
    
    @staticmethod
    def reset_otp_attempts(db: Session, pending_user: PendingUser) -> None:
        """Reset OTP attempts for a pending user (called on successful verification)."""
        pending_user.otp_attempts = 0
        pending_user.otp_locked_until = None
        db.commit()
        logger.info(f"OTP attempts reset for user {pending_user.email}")
    
    @staticmethod
    def update_pending_user_otp_status(
        db: Session, 
        pending_user: PendingUser, 
        increment_attempts: bool = True
    ) -> Dict[str, Any]:
        """Update pending user OTP status and return current lockout information."""
        if increment_attempts:
            return PendingUserUtils.increment_otp_attempts(db, pending_user)
        else:
            return PendingUserUtils.check_otp_lockout_status(pending_user)
