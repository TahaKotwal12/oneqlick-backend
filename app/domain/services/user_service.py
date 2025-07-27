from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
import bcrypt
from app.infra.db.postgres.repositories.user_repository import UserRepository
from app.infra.db.postgres.models.user import User, UserRole, UserStatus
from app.api.schemas.user_schema import UserCreateRequest, UserUpdateRequest
from app.config.logger import get_logger

logger = get_logger(__name__)

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt with salt."""
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        return password_hash.decode('utf-8')

    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against bcrypt hash."""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        except Exception as e:
            logger.error(f"Error verifying password: {str(e)}")
            return False

    def create_user(self, user_data: UserCreateRequest) -> User:
        """Create a new user with bcrypt hashed password."""
        try:
            # Check if user already exists
            existing_user = self.user_repository.get_user_by_email(user_data.email)
            if existing_user:
                raise ValueError("User with this email already exists")
                
            existing_phone = self.user_repository.get_user_by_phone(user_data.phone)
            if existing_phone:
                raise ValueError("User with this phone number already exists")

            # Hash password using bcrypt
            password_hash = self._hash_password(user_data.password)

            # Prepare user data
            user_dict = {
                "email": user_data.email,
                "phone": user_data.phone,
                "password_hash": password_hash,
                "first_name": user_data.first_name,
                "last_name": user_data.last_name,
                "role": user_data.role,
                "profile_image": user_data.profile_image
            }

            user = self.user_repository.create_user(user_dict)
            logger.info(f"User created successfully with bcrypt password: {user.user_id}")
            return user

        except ValueError as e:
            logger.warning(f"User creation validation error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise

    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        try:
            user = self.user_repository.get_user_by_id(user_id)
            if not user:
                logger.warning(f"User not found: {user_id}")
            return user
        except Exception as e:
            logger.error(f"Error retrieving user: {str(e)}")
            raise

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.user_repository.get_user_by_email(email)

    def update_user(self, user_id: UUID, update_data: UserUpdateRequest) -> Optional[User]:
        """Update user information."""
        try:
            # Convert Pydantic model to dict, excluding None values
            update_dict = update_data.model_dump(exclude_unset=True, exclude_none=True)
            
            if not update_dict:
                raise ValueError("No data provided for update")

            user = self.user_repository.update_user(user_id, update_dict)
            if user:
                logger.info(f"User updated successfully: {user_id}")
            return user

        except ValueError as e:
            logger.warning(f"User update validation error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            raise

    def delete_user(self, user_id: UUID) -> bool:
        """Soft delete user."""
        try:
            result = self.user_repository.delete_user(user_id)
            if result:
                logger.info(f"User deleted successfully: {user_id}")
            return result
        except Exception as e:
            logger.error(f"Error deleting user: {str(e)}")
            raise

    def get_all_users(self, skip: int = 0, limit: int = 100, role: Optional[str] = None, status: Optional[str] = None) -> List[User]:
        """Get all users with optional filtering."""
        try:
            # Convert string enums to enum types if provided
            role_enum = UserRole(role) if role else None
            status_enum = UserStatus(status) if status else None
            
            users = self.user_repository.get_all_users(skip=skip, limit=limit, role=role_enum, status=status_enum)
            logger.info(f"Retrieved {len(users)} users")
            return users
        except ValueError as e:
            logger.warning(f"Invalid enum value: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error retrieving users: {str(e)}")
            raise

    def verify_user_email(self, user_id: UUID) -> bool:
        """Verify user email."""
        return self.user_repository.verify_email(user_id)

    def verify_user_phone(self, user_id: UUID) -> bool:
        """Verify user phone."""
        return self.user_repository.verify_phone(user_id)

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password using bcrypt."""
        try:
            user = self.user_repository.get_user_by_email(email)
            if not user:
                logger.warning(f"User not found for authentication: {email}")
                return None

            if user.status != UserStatus.active:
                logger.warning(f"Inactive user attempted login: {email}")
                return None

            if self._verify_password(password, user.password_hash):
                logger.info(f"User authenticated successfully with bcrypt: {email}")
                return user
            else:
                logger.warning(f"Invalid password for user: {email}")
                return None

        except Exception as e:
            logger.error(f"Error authenticating user: {str(e)}")
            raise
        