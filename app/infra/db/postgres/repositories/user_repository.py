from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.infra.db.postgres.models.user import User, UserRole, UserStatus
from app.config.logger import get_logger

logger = get_logger(__name__)

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: dict) -> User:
        """Create a new user in the database."""
        try:
            user = User(**user_data)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            logger.info(f"User created successfully with ID: {user.user_id}")
            return user
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Integrity error creating user: {str(e)}")
            raise ValueError("Email or phone already exists")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating user: {str(e)}")
            raise

    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        try:
            user = self.db.query(User).filter(User.user_id == user_id).first()
            if user:
                logger.info(f"User retrieved successfully: {user_id}")
            else:
                logger.warning(f"User not found: {user_id}")
            return user
        except Exception as e:
            logger.error(f"Error retrieving user by ID {user_id}: {str(e)}")
            raise

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        try:
            user = self.db.query(User).filter(User.email == email).first()
            return user
        except Exception as e:
            logger.error(f"Error retrieving user by email {email}: {str(e)}")
            raise

    def get_user_by_phone(self, phone: str) -> Optional[User]:
        """Get user by phone."""
        try:
            user = self.db.query(User).filter(User.phone == phone).first()
            return user
        except Exception as e:
            logger.error(f"Error retrieving user by phone {phone}: {str(e)}")
            raise

    def update_user(self, user_id: UUID, update_data: dict) -> Optional[User]:
        """Update user information."""
        try:
            user = self.db.query(User).filter(User.user_id == user_id).first()
            if not user:
                logger.warning(f"User not found for update: {user_id}")
                return None

            for key, value in update_data.items():
                if hasattr(user, key) and value is not None:
                    setattr(user, key, value)

            self.db.commit()
            self.db.refresh(user)
            logger.info(f"User updated successfully: {user_id}")
            return user
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Integrity error updating user: {str(e)}")
            raise ValueError("Email or phone already exists")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating user {user_id}: {str(e)}")
            raise

    def delete_user(self, user_id: UUID) -> bool:
        """Soft delete user by setting status to inactive."""
        try:
            user = self.db.query(User).filter(User.user_id == user_id).first()
            if not user:
                logger.warning(f"User not found for deletion: {user_id}")
                return False

            user.status = UserStatus.inactive
            self.db.commit()
            logger.info(f"User soft deleted successfully: {user_id}")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting user {user_id}: {str(e)}")
            raise

    def get_all_users(self, skip: int = 0, limit: int = 100, role: Optional[UserRole] = None, status: Optional[UserStatus] = None) -> List[User]:
        """Get all users with optional filtering."""
        try:
            query = self.db.query(User)
            
            if role:
                query = query.filter(User.role == role)
            if status:
                query = query.filter(User.status == status)
                
            users = query.offset(skip).limit(limit).all()
            logger.info(f"Retrieved {len(users)} users")
            return users
        except Exception as e:
            logger.error(f"Error retrieving users: {str(e)}")
            raise

    def verify_email(self, user_id: UUID) -> bool:
        """Mark user email as verified."""
        try:
            user = self.db.query(User).filter(User.user_id == user_id).first()
            if not user:
                return False
                
            user.email_verified = True
            self.db.commit()
            logger.info(f"Email verified for user: {user_id}")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error verifying email for user {user_id}: {str(e)}")
            raise

    def verify_phone(self, user_id: UUID) -> bool:
        """Mark user phone as verified."""
        try:
            user = self.db.query(User).filter(User.user_id == user_id).first()
            if not user:
                return False
                
            user.phone_verified = True
            self.db.commit()
            logger.info(f"Phone verified for user: {user_id}")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error verifying phone for user {user_id}: {str(e)}")
            raise 