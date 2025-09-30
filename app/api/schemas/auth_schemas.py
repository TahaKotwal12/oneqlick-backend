from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

# Request Schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)

class SignupRequest(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=20)
    password: str = Field(..., min_length=6, max_length=100)

class GoogleSigninRequest(BaseModel):
    id_token: str
    device_info: Dict[str, Any]

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class SendOTPRequest(BaseModel):
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    otp_type: str = Field(..., pattern="^(phone_verification|email_verification|password_reset)$")

class VerifyOTPRequest(BaseModel):
    otp_code: str = Field(..., min_length=4, max_length=10)
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    otp_type: str = Field(..., pattern="^(phone_verification|email_verification|password_reset)$")

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    otp_code: str = Field(..., min_length=4, max_length=10)
    email: EmailStr
    new_password: str = Field(..., min_length=6, max_length=100)

class LogoutRequest(BaseModel):
    refresh_token: Optional[str] = None
    logout_all_devices: bool = False

# Response Schemas
class UserResponse(BaseModel):
    user_id: UUID
    email: str
    phone: str
    first_name: str
    last_name: str
    role: str
    status: str
    profile_image: Optional[str] = None
    email_verified: bool
    phone_verified: bool
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    loyalty_points: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class LoginResponse(BaseModel):
    user: UserResponse
    tokens: TokenResponse
    is_new_user: bool = False
    requires_verification: bool = False

class SignupResponse(BaseModel):
    user: UserResponse
    tokens: Optional[TokenResponse] = None
    requires_verification: bool = True

class GoogleSigninResponse(BaseModel):
    user: UserResponse
    tokens: TokenResponse
    is_new_user: bool
    requires_verification: bool = False

class RefreshTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class SendOTPResponse(BaseModel):
    message: str
    expires_in: int
    phone: Optional[str] = None
    email: Optional[str] = None

class VerifyOTPResponse(BaseModel):
    verified: bool
    message: str
    requires_profile_completion: bool = False

class LogoutResponse(BaseModel):
    message: str
    logged_out_devices: int

class UserSessionResponse(BaseModel):
    session_id: UUID
    device_name: Optional[str] = None
    device_type: Optional[str] = None
    platform: Optional[str] = None
    app_version: Optional[str] = None
    last_activity: datetime
    is_current: bool

class UserSessionsResponse(BaseModel):
    sessions: list[UserSessionResponse]
    total_sessions: int

# Device Info Schema
class DeviceInfo(BaseModel):
    device_id: str
    device_name: str
    device_type: str
    platform: str
    app_version: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
