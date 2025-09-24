from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID
from app.utils.enums import UserRole, UserStatus, Gender, AddressType

# Request Schemas
class UserUpdateRequest(BaseModel):
    """Request schema for updating user profile"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    profile_image: Optional[str] = Field(None, max_length=500)
    
    class Config:
        use_enum_values = True

    @validator('phone')
    def validate_phone(cls, v):
        if v is not None:
            # Remove any non-digit characters for validation
            phone_digits = ''.join(filter(str.isdigit, v))
            if len(phone_digits) < 10 or len(phone_digits) > 15:
                raise ValueError('Phone number must be between 10 and 15 digits')
        return v
    
    @validator('gender')
    def validate_gender(cls, v):
        if v is not None:
            # Ensure gender is lowercase
            if isinstance(v, str):
                v = v.lower()
            # Validate against enum values
            valid_genders = ['male', 'female', 'other']
            if v not in valid_genders:
                raise ValueError(f'Gender must be one of: {", ".join(valid_genders)}')
        return v

class PasswordChangeRequest(BaseModel):
    """Request schema for changing password"""
    current_password: str = Field(..., min_length=6, max_length=100)
    new_password: str = Field(..., min_length=6, max_length=100)

class AddressCreateRequest(BaseModel):
    """Request schema for creating user address"""
    title: str = Field(..., min_length=1, max_length=100)
    address_line1: str = Field(..., min_length=1, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=1, max_length=100)
    postal_code: str = Field(..., min_length=1, max_length=20)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    is_default: bool = False
    address_type: AddressType = AddressType.HOME
    landmark: Optional[str] = Field(None, max_length=255)

class AddressUpdateRequest(BaseModel):
    """Request schema for updating user address"""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    address_line1: Optional[str] = Field(None, min_length=1, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, min_length=1, max_length=100)
    postal_code: Optional[str] = Field(None, min_length=1, max_length=20)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    is_default: Optional[bool] = None
    address_type: Optional[AddressType] = None
    landmark: Optional[str] = Field(None, max_length=255)

class UserPreferencesRequest(BaseModel):
    """Request schema for updating user preferences"""
    email_notifications: Optional[bool] = None
    sms_notifications: Optional[bool] = None
    push_notifications: Optional[bool] = None
    marketing_emails: Optional[bool] = None
    language: Optional[str] = Field(None, max_length=10)
    currency: Optional[str] = Field(None, max_length=3)

# Response Schemas
class AddressResponse(BaseModel):
    """Response schema for user address"""
    address_id: UUID
    title: str
    address_line1: str
    address_line2: Optional[str]
    city: str
    state: str
    postal_code: str
    latitude: Optional[float]
    longitude: Optional[float]
    is_default: bool
    address_type: AddressType
    landmark: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    """Response schema for user profile"""
    user_id: UUID
    email: str
    phone: str
    first_name: str
    last_name: str
    role: str
    status: str
    profile_image: Optional[str]
    email_verified: bool
    phone_verified: bool
    date_of_birth: Optional[date]
    gender: Optional[Gender]
    loyalty_points: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        use_enum_values = True

class UserProfileResponse(BaseModel):
    """Extended user profile response with addresses"""
    user: UserResponse
    addresses: List[AddressResponse]
    preferences: Optional[dict] = None

class UserStatsResponse(BaseModel):
    """User statistics response"""
    total_orders: int
    total_spent: float
    loyalty_points: int
    member_since: datetime
    favorite_cuisines: List[str]
    last_order_date: Optional[datetime]

class UserSessionResponse(BaseModel):
    """User session response"""
    session_id: UUID
    device_name: Optional[str]
    device_type: Optional[str]
    platform: Optional[str]
    app_version: Optional[str]
    last_activity: datetime
    is_active: bool

    class Config:
        from_attributes = True

class UserSessionsResponse(BaseModel):
    """User sessions list response"""
    sessions: List[UserSessionResponse]
    total_sessions: int

class UserListResponse(BaseModel):
    """User list response for admin"""
    users: List[UserResponse]
    total_users: int
    page: int
    page_size: int
    total_pages: int

class UserSearchRequest(BaseModel):
    """Request schema for searching users (admin only)"""
    query: Optional[str] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)

class UserStatusUpdateRequest(BaseModel):
    """Request schema for updating user status (admin only)"""
    status: UserStatus
    reason: Optional[str] = Field(None, max_length=500)

class UserRoleUpdateRequest(BaseModel):
    """Request schema for updating user role (admin only)"""
    role: UserRole
    reason: Optional[str] = Field(None, max_length=500)

# Pagination schemas
class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Number of items per page")

class PaginatedResponse(BaseModel):
    """Paginated response wrapper"""
    items: List[BaseModel]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool
