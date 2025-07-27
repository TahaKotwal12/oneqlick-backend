from pydantic import BaseModel, Field, EmailStr
from uuid import UUID
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    customer = 'customer'
    admin = 'admin'
    delivery_partner = 'delivery_partner'
    restaurant_owner = 'restaurant_owner'

class UserStatus(str, Enum):
    active = 'active'
    inactive = 'inactive'
    suspended = 'suspended'

class UserCreateRequest(BaseModel):
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=20)
    password: str = Field(..., min_length=6)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    role: UserRole
    profile_image: Optional[str] = None

class UserUpdateRequest(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    profile_image: Optional[str] = None
    status: Optional[UserStatus] = None

class UserResponse(BaseModel):
    user_id: UUID
    email: str
    phone: str
    first_name: str
    last_name: str
    role: UserRole
    status: UserStatus
    profile_image: Optional[str] = None
    email_verified: bool
    phone_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserListResponse(BaseModel):
    user_id: UUID
    email: str
    first_name: str
    last_name: str
    role: UserRole
    status: UserStatus
    email_verified: bool
    phone_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True