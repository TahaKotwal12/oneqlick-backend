import secrets
import string
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.infra.db.postgres.models.otp_verification import OTPVerification
from app.infra.db.postgres.models.user import User
from app.utils.enums import UserRole, UserStatus
import logging

logger = logging.getLogger(__name__)

class OTPUtils:
    """Utility class for OTP generation, validation, and management"""
    
    # OTP Configuration
    OTP_LENGTH = 6
    OTP_EXPIRY_MINUTES = 10
    MAX_ATTEMPTS = 3
    OTP_CHARS = string.digits  # Only numeric OTPs
    
    @staticmethod
    def generate_otp() -> str:
        """Generate a random OTP code"""
        return ''.join(secrets.choice(OTPUtils.OTP_CHARS) for _ in range(OTPUtils.OTP_LENGTH))
    
    @staticmethod
    def get_otp_expiry() -> datetime:
        """Get OTP expiry timestamp"""
        return datetime.now(timezone.utc) + timedelta(minutes=OTPUtils.OTP_EXPIRY_MINUTES)
    
    @staticmethod
    def is_otp_expired(expires_at: datetime) -> bool:
        """Check if OTP is expired"""
        now = datetime.now(timezone.utc)
        
        # Ensure expires_at is timezone-aware
        if expires_at.tzinfo is None:
            # If timezone-naive, assume it's UTC
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        
        # Ensure both datetimes are timezone-aware for comparison
        if now.tzinfo is None:
            now = now.replace(tzinfo=timezone.utc)
        
        return now > expires_at
    
    @staticmethod
    def create_otp_record(
        db: Session,
        user_id: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        otp_type: str = "email_verification",
        is_pending_user: bool = False
    ) -> Optional[OTPVerification]:
        """Create a new OTP record"""
        try:
            # Invalidate any existing OTPs for this user and type
            OTPUtils.invalidate_existing_otps(db, user_id, otp_type, email, phone)
            
            # Generate new OTP
            otp_code = OTPUtils.generate_otp()
            expires_at = OTPUtils.get_otp_expiry()
            
            # Create OTP record with appropriate user reference
            if is_pending_user:
                otp_record = OTPVerification(
                    pending_user_id=user_id,  # Use pending_user_id for pending users
                    email=email,
                    phone=phone,
                    otp_code=otp_code,
                    otp_type=otp_type,
                    expires_at=expires_at,
                    is_verified=False,
                    attempts=0,
                    max_attempts=OTPUtils.MAX_ATTEMPTS
                )
            else:
                otp_record = OTPVerification(
                    user_id=user_id,  # Use user_id for regular users
                    email=email,
                    phone=phone,
                    otp_code=otp_code,
                    otp_type=otp_type,
                    expires_at=expires_at,
                    is_verified=False,
                    attempts=0,
                    max_attempts=OTPUtils.MAX_ATTEMPTS
                )
            
            db.add(otp_record)
            db.commit()
            db.refresh(otp_record)
            
            logger.info(f"OTP record created for {'pending' if is_pending_user else 'regular'} user {user_id}, type: {otp_type}")
            return otp_record
            
        except Exception as e:
            logger.error(f"Failed to create OTP record: {e}")
            db.rollback()
            return None
    
    @staticmethod
    def invalidate_existing_otps(
        db: Session,
        user_id: str,
        otp_type: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        is_pending_user: bool = False
    ) -> None:
        """Invalidate existing OTPs for the same user and type"""
        try:
            # Build query conditions based on user type
            if is_pending_user:
                conditions = [
                    OTPVerification.pending_user_id == user_id,
                    OTPVerification.otp_type == otp_type,
                    OTPVerification.is_verified == False
                ]
            else:
                conditions = [
                    OTPVerification.user_id == user_id,
                    OTPVerification.otp_type == otp_type,
                    OTPVerification.is_verified == False
                ]
            
            # Add email/phone conditions if provided
            if email:
                conditions.append(OTPVerification.email == email)
            if phone:
                conditions.append(OTPVerification.phone == phone)
            
            # Find and invalidate existing OTPs
            existing_otps = db.query(OTPVerification).filter(and_(*conditions)).all()
            
            for otp in existing_otps:
                otp.is_verified = True  # Mark as used/invalid
                otp.attempts = otp.max_attempts  # Mark as exhausted
            
            db.commit()
            logger.info(f"Invalidated {len(existing_otps)} existing OTPs for user {user_id}")
            
        except Exception as e:
            logger.error(f"Failed to invalidate existing OTPs: {e}")
            db.rollback()
    
    @staticmethod
    def verify_otp(
        db: Session,
        otp_code: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        otp_type: str = "email_verification"
    ) -> Dict[str, Any]:
        """Verify OTP code"""
        try:
            # Build query conditions
            conditions = [
                OTPVerification.otp_code == otp_code,
                OTPVerification.otp_type == otp_type,
                OTPVerification.is_verified == False
            ]
            
            # Add email/phone conditions
            if email:
                conditions.append(OTPVerification.email == email)
            if phone:
                conditions.append(OTPVerification.phone == phone)
            
            # Find OTP record
            otp_record = db.query(OTPVerification).filter(and_(*conditions)).first()
            
            if not otp_record:
                return {
                    "success": False,
                    "message": "Invalid OTP code",
                    "error_code": "INVALID_OTP"
                }
            
            # Check if OTP is expired
            if OTPUtils.is_otp_expired(otp_record.expires_at):
                return {
                    "success": False,
                    "message": "OTP has expired",
                    "error_code": "OTP_EXPIRED"
                }
            
            # Check if max attempts exceeded
            if otp_record.attempts >= otp_record.max_attempts:
                return {
                    "success": False,
                    "message": "Maximum attempts exceeded",
                    "error_code": "MAX_ATTEMPTS_EXCEEDED"
                }
            
            # Verify OTP
            otp_record.is_verified = True
            otp_record.attempts += 1
            db.commit()
            
            # Determine which user_id to return
            actual_user_id = otp_record.user_id if otp_record.user_id else otp_record.pending_user_id
            is_pending = otp_record.pending_user_id is not None
            
            logger.info(f"OTP verified successfully for {'pending' if is_pending else 'regular'} user {actual_user_id}")
            
            return {
                "success": True,
                "message": "OTP verified successfully",
                "user_id": str(actual_user_id),
                "is_pending_user": is_pending,
                "otp_record": otp_record
            }
            
        except Exception as e:
            logger.error(f"Failed to verify OTP: {e}")
            db.rollback()
            return {
                "success": False,
                "message": "OTP verification failed",
                "error_code": "VERIFICATION_ERROR"
            }
    
    @staticmethod
    def increment_otp_attempts(
        db: Session,
        otp_code: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        otp_type: str = "email_verification"
    ) -> bool:
        """Increment OTP attempts counter"""
        try:
            # Build query conditions
            conditions = [
                OTPVerification.otp_code == otp_code,
                OTPVerification.otp_type == otp_type,
                OTPVerification.is_verified == False
            ]
            
            if email:
                conditions.append(OTPVerification.email == email)
            if phone:
                conditions.append(OTPVerification.phone == phone)
            
            # Find OTP record
            otp_record = db.query(OTPVerification).filter(and_(*conditions)).first()
            
            if otp_record and not OTPUtils.is_otp_expired(otp_record.expires_at):
                otp_record.attempts += 1
                db.commit()
                logger.info(f"Incremented OTP attempts for user {otp_record.user_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to increment OTP attempts: {e}")
            db.rollback()
            return False
    
    @staticmethod
    def get_user_by_otp_identifier(
        db: Session,
        email: Optional[str] = None,
        phone: Optional[str] = None
    ) -> Optional[User]:
        """Get user by email or phone for OTP verification"""
        try:
            if email:
                return db.query(User).filter(User.email == email).first()
            elif phone:
                return db.query(User).filter(User.phone == phone).first()
            return None
        except Exception as e:
            logger.error(f"Failed to get user by identifier: {e}")
            return None
    
    @staticmethod
    def cleanup_expired_otps(db: Session) -> int:
        """Clean up expired OTP records (can be run as a scheduled task)"""
        try:
            expired_otps = db.query(OTPVerification).filter(
                OTPVerification.expires_at < datetime.now(timezone.utc)
            ).all()
            
            count = len(expired_otps)
            for otp in expired_otps:
                db.delete(otp)
            
            db.commit()
            logger.info(f"Cleaned up {count} expired OTP records")
            return count
            
        except Exception as e:
            logger.error(f"Failed to cleanup expired OTPs: {e}")
            db.rollback()
            return 0
    
    @staticmethod
    def get_otp_stats(db: Session, user_id: str) -> Dict[str, Any]:
        """Get OTP statistics for a user"""
        try:
            total_otps = db.query(OTPVerification).filter(
                OTPVerification.user_id == user_id
            ).count()
            
            verified_otps = db.query(OTPVerification).filter(
                and_(
                    OTPVerification.user_id == user_id,
                    OTPVerification.is_verified == True
                )
            ).count()
            
            pending_otps = db.query(OTPVerification).filter(
                and_(
                    OTPVerification.user_id == user_id,
                    OTPVerification.is_verified == False,
                    OTPVerification.expires_at > datetime.now(timezone.utc)
                )
            ).count()
            
            return {
                "total_otps": total_otps,
                "verified_otps": verified_otps,
                "pending_otps": pending_otps,
                "success_rate": (verified_otps / total_otps * 100) if total_otps > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Failed to get OTP stats: {e}")
            return {
                "total_otps": 0,
                "verified_otps": 0,
                "pending_otps": 0,
                "success_rate": 0
            }
