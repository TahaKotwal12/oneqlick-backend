from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class DeliveryPartnerAdminResponse(BaseModel):
    """Admin view of a delivery partner's details"""
    delivery_partner_id: UUID
    user_id: UUID
    first_name: str
    last_name: str
    email: str
    phone: str
    profile_image: Optional[str] = None
    vehicle_type: str
    vehicle_number: str
    license_number: str
    availability_status: str
    status: str  
    total_deliveries: int
    rating: Optional[float] = None
    address: Optional[str] = None  
    created_at: datetime

    class Config:
        from_attributes = True

class DeliveryPartnerAdminListResponse(BaseModel):
    """List of delivery partners for admin"""
    delivery_partners: List[DeliveryPartnerAdminResponse]
    total_count: int

class DeliveryPartnerAdminUpdateRequest(BaseModel):
    """Request payload to edit a delivery partner"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    vehicle_type: Optional[str] = None
    vehicle_number: Optional[str] = Field(None, max_length=50)
    license_number: Optional[str] = Field(None, max_length=50)
    availability_status: Optional[str] = None
