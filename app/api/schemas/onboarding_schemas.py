from pydantic import BaseModel, Field, validator, EmailStr
from typing import List, Optional, Dict
from datetime import datetime, time
from decimal import Decimal
from uuid import UUID


# ============================================================================
# REGISTRATION SCHEMAS
# ============================================================================

class RestaurantRegistrationRequest(BaseModel):
    """Request schema for restaurant owner registration."""
    # User details
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=20)
    password: str = Field(..., min_length=8)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    
    # Restaurant basic info
    restaurant_name: str = Field(..., min_length=1, max_length=255)
    business_type: str  # cloud_kitchen, dine_in, both
    cuisine_type: str = Field(..., max_length=100)
    estimated_daily_orders: Optional[int] = Field(None, ge=0)

    @validator('business_type')
    def validate_business_type(cls, v):
        allowed = ['cloud_kitchen', 'dine_in', 'both']
        if v not in allowed:
            raise ValueError(f'business_type must be one of {allowed}')
        return v


class RestaurantRegistrationResponse(BaseModel):
    """Response schema for restaurant registration."""
    success: bool
    message: str
    user_id: UUID
    onboarding_id: UUID
    email: str
    phone: str


# ============================================================================
# ONBOARDING PROGRESS SCHEMAS
# ============================================================================

class OnboardingProgressResponse(BaseModel):
    """Response schema for onboarding progress."""
    onboarding_id: UUID
    user_id: UUID
    restaurant_id: Optional[UUID]
    current_step: str
    completion_percentage: int
    verification_status: str
    
    # Step completion flags
    steps_completed: Dict[str, bool] = Field(
        description="Dictionary of step completion status"
    )
    
    # Timestamps
    started_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# ============================================================================
# DOCUMENT UPLOAD SCHEMAS
# ============================================================================

class DocumentUploadRequest(BaseModel):
    """Request schema for document upload."""
    document_type: str  # fssai, gst, pan, bank_proof
    document_url: str = Field(..., max_length=500)

    @validator('document_type')
    def validate_document_type(cls, v):
        allowed = ['fssai', 'gst', 'pan', 'bank_proof']
        if v not in allowed:
            raise ValueError(f'document_type must be one of {allowed}')
        return v


class DocumentUploadResponse(BaseModel):
    """Response schema for document upload."""
    success: bool
    message: str
    document_type: str
    document_url: str
    documents_uploaded: bool


# ============================================================================
# PROFILE SETUP SCHEMAS
# ============================================================================

class RestaurantProfileSetupRequest(BaseModel):
    """Request schema for restaurant profile setup."""
    description: str = Field(..., max_length=1000)
    address_line1: str = Field(..., max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: str = Field(..., max_length=100)
    state: str = Field(..., max_length=100)
    postal_code: str = Field(..., max_length=20)
    latitude: Decimal = Field(..., ge=-90, le=90)
    longitude: Decimal = Field(..., ge=-180, le=180)
    
    # Restaurant details
    image_url: Optional[str] = Field(None, max_length=500)
    cover_image_url: Optional[str] = Field(None, max_length=500)
    opening_time: time
    closing_time: time
    min_order_amount: Decimal = Field(..., ge=0)
    delivery_fee: Decimal = Field(..., ge=0)
    is_pure_veg: bool = False
    cost_for_two: Optional[Decimal] = Field(None, ge=0)
    avg_delivery_time: Optional[int] = Field(None, ge=0)  # in minutes


class RestaurantProfileSetupResponse(BaseModel):
    """Response schema for profile setup."""
    success: bool
    message: str
    restaurant_id: UUID
    profile_completed: bool


# ============================================================================
# BANK DETAILS SCHEMAS
# ============================================================================

class BankDetailsRequest(BaseModel):
    """Request schema for bank details."""
    account_number: str = Field(..., min_length=9, max_length=18)
    ifsc_code: str = Field(..., min_length=11, max_length=11)
    account_holder_name: str = Field(..., min_length=1, max_length=255)
    bank_name: str = Field(..., min_length=1, max_length=255)
    
    # Business registration numbers
    fssai_license_number: Optional[str] = Field(None, max_length=50)
    gst_number: Optional[str] = Field(None, max_length=50)
    pan_number: Optional[str] = Field(None, max_length=50)

    @validator('ifsc_code')
    def validate_ifsc(cls, v):
        if not v.isalnum():
            raise ValueError('IFSC code must be alphanumeric')
        return v.upper()


class BankDetailsResponse(BaseModel):
    """Response schema for bank details."""
    success: bool
    message: str
    bank_details_added: bool


# ============================================================================
# BULK MENU UPLOAD SCHEMAS
# ============================================================================

class MenuItemImportRow(BaseModel):
    """Schema for a single menu item row from CSV."""
    name: str = Field(..., min_length=1, max_length=255)
    category_name: str = Field(..., min_length=1, max_length=100)  # Changed from category_id
    price: Decimal = Field(..., gt=0)
    description: Optional[str] = Field(None, max_length=1000)
    is_veg: bool = True
    image_url: Optional[str] = Field(None, max_length=500)
    prep_time: Optional[int] = Field(None, ge=0)



class BulkMenuUploadRequest(BaseModel):
    """Request schema for bulk menu upload."""
    csv_data: str = Field(..., description="CSV content as string")


class MenuItemError(BaseModel):
    """Schema for menu item import error."""
    row_number: int
    item_name: Optional[str]
    error: str


class BulkMenuUploadResponse(BaseModel):
    """Response schema for bulk menu upload."""
    success: bool
    message: str
    total_rows: int
    success_count: int
    error_count: int
    errors: List[MenuItemError] = []
    menu_uploaded: bool


# ============================================================================
# ONBOARDING SUBMISSION SCHEMAS
# ============================================================================

class OnboardingSubmitResponse(BaseModel):
    """Response schema for onboarding submission."""
    success: bool
    message: str
    onboarding_id: UUID
    verification_status: str
    submitted_at: datetime


# ============================================================================
# ADMIN APPROVAL SCHEMAS
# ============================================================================

class OnboardingApprovalRequest(BaseModel):
    """Request schema for admin approval."""
    notes: Optional[str] = Field(None, max_length=1000)


class OnboardingRejectionRequest(BaseModel):
    """Request schema for admin rejection."""
    reason: str = Field(..., min_length=10, max_length=500)


class OnboardingDetailResponse(BaseModel):
    """Detailed onboarding information for admin."""
    onboarding_id: UUID
    user_id: UUID
    restaurant_id: Optional[UUID]
    
    # User info
    owner_name: str
    email: str
    phone: str
    
    # Restaurant info
    restaurant_name: str
    business_type: str
    cuisine_type: str
    
    # Progress
    current_step: str
    completion_percentage: int
    verification_status: str
    
    # Documents
    fssai_license_url: Optional[str]
    gst_certificate_url: Optional[str]
    pan_card_url: Optional[str]
    bank_proof_url: Optional[str]
    
    # Business details
    fssai_license_number: Optional[str]
    gst_number: Optional[str]
    pan_number: Optional[str]
    
    # Bank details
    bank_account_number: Optional[str]
    bank_ifsc_code: Optional[str]
    bank_account_holder_name: Optional[str]
    bank_name: Optional[str]
    
    # Timestamps
    started_at: datetime
    completed_at: Optional[datetime]
    verified_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class PendingOnboardingListResponse(BaseModel):
    """Response schema for pending onboarding list."""
    total_count: int
    pending_count: int
    in_review_count: int
    onboardings: List[OnboardingDetailResponse]
