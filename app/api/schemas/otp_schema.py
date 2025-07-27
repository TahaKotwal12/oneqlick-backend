from pydantic import BaseModel, Field, validator
from typing import Optional

class OTPRequestSchema(BaseModel):
    phone: str = Field(..., min_length=10, max_length=20, description="Phone number to send OTP to")
    
    @validator('phone')
    def validate_phone(cls, v):
        # Remove all non-digit characters for validation
        digits_only = ''.join(filter(str.isdigit, v))
        if len(digits_only) < 7 or len(digits_only) > 15:
            raise ValueError('Phone number must be between 7 and 15 digits')
        return v

class OTPVerifySchema(BaseModel):
    phone: str = Field(..., min_length=10, max_length=20, description="Phone number")
    otp: str = Field(..., min_length=4, max_length=8, description="OTP code to verify")
    
    @validator('phone')
    def validate_phone(cls, v):
        digits_only = ''.join(filter(str.isdigit, v))
        if len(digits_only) < 7 or len(digits_only) > 15:
            raise ValueError('Phone number must be between 7 and 15 digits')
        return v
    
    @validator('otp')
    def validate_otp(cls, v):
        if not v.isdigit():
            raise ValueError('OTP must contain only digits')
        return v

class OTPResponseSchema(BaseModel):
    success: bool
    message: str
    phone: str
    expires_in_minutes: Optional[int] = None
    attempts_remaining: Optional[int] = None

class OTPVerifyResponseSchema(BaseModel):
    success: bool
    message: str
    phone: str
    verified: bool 