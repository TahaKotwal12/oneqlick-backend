from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from enum import Enum

class AuthProvider(str, Enum):
    google = 'google'
    facebook = 'facebook'
    apple = 'apple'

class OTPType(str, Enum):
    phone_verification = 'phone_verification'
    email_verification = 'email_verification'
    password_reset = 'password_reset'

# ====================================================================
# REQUEST SCHEMAS
# ====================================================================

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    device_info: Optional[Dict[str, Any]] = None

class SignupRequest(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=20)
    password: str = Field(..., min_length=6, max_length=100)
    device_info: Optional[Dict[str, Any]] = None

    @validator('phone')
    def validate_phone(cls, v):
        # Basic phone validation - can be enhanced
        if not v.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise ValueError('Phone number must contain only digits, +, -, and spaces')
        return v

class GoogleSignInRequest(BaseModel):
    id_token: str = Field(..., min_length=1)
    device_info: Optional[Dict[str, Any]] = None

class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., min_length=1)

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=6, max_length=100)

class VerifyOTPRequest(BaseModel):
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    email: Optional[EmailStr] = None
    otp_code: str = Field(..., min_length=4, max_length=10)
    otp_type: OTPType

class ResendOTPRequest(BaseModel):
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    email: Optional[EmailStr] = None
    otp_type: OTPType

class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=6, max_length=100)
    new_password: str = Field(..., min_length=6, max_length=100)

class LogoutRequest(BaseModel):
    refresh_token: Optional[str] = None
    logout_all_devices: bool = False

# ====================================================================
# RESPONSE SCHEMAS
# ====================================================================

class AuthTokensResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int  # seconds

class UserProfileResponse(BaseModel):
    user_id: UUID
    first_name: str
    last_name: str
    email: str
    phone: str
    profile_image: Optional[str] = None
    email_verified: bool
    phone_verified: bool
    role: str
    status: str
    created_at: datetime
    updated_at: datetime

class LoginResponse(BaseModel):
    user: UserProfileResponse
    tokens: AuthTokensResponse
    is_new_user: bool = False

class SignupResponse(BaseModel):
    user: UserProfileResponse
    tokens: AuthTokensResponse
    requires_verification: bool = True

class GoogleSignInResponse(BaseModel):
    user: UserProfileResponse
    tokens: AuthTokensResponse
    is_new_user: bool = False
    requires_verification: bool = False

class RefreshTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int

class OTPResponse(BaseModel):
    message: str
    expires_in: int  # seconds
    phone: Optional[str] = None
    email: Optional[str] = None

class VerifyOTPResponse(BaseModel):
    verified: bool
    message: str
    requires_profile_completion: bool = False

class PasswordResetResponse(BaseModel):
    message: str
    email: str

class LogoutResponse(BaseModel):
    message: str
    logged_out_devices: int = 0

class SessionInfo(BaseModel):
    session_id: UUID
    device_name: Optional[str]
    device_type: Optional[str]
    platform: Optional[str]
    app_version: Optional[str]
    last_activity: datetime
    is_current: bool = False

class UserSessionsResponse(BaseModel):
    sessions: list[SessionInfo]
    total_sessions: int

# ====================================================================
# INTERNAL SCHEMAS (for service layer)
# ====================================================================

class TokenData(BaseModel):
    user_id: UUID
    email: str
    role: str
    session_id: Optional[UUID] = None

class DeviceInfo(BaseModel):
    device_id: str
    device_name: Optional[str] = None
    device_type: Optional[str] = None
    platform: Optional[str] = None
    app_version: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class OTPData(BaseModel):
    phone: Optional[str] = None
    email: Optional[str] = None
    otp_code: str
    otp_type: OTPType
    expires_at: datetime
    attempts: int = 0
    max_attempts: int = 3

class GoogleUserInfo(BaseModel):
    google_id: str
    email: str
    name: str
    given_name: str
    family_name: str
    picture: Optional[str] = None
    verified_email: bool = True
