from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..base import Base


class RestaurantOnboarding(Base):
    """Restaurant onboarding tracking model."""
    __tablename__ = 'core_mstr_one_qlick_restaurant_onboarding_tbl'

    onboarding_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl.user_id'), nullable=False)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_restaurants_tbl.restaurant_id'))
    
    # Progress tracking
    current_step = Column(String(50), default='registration', nullable=False)  # registration, verification, profile, menu, bank_details, review, completed
    completion_percentage = Column(Integer, default=0, nullable=False)
    
    # Step completion flags
    registration_completed = Column(Boolean, default=False, nullable=False)
    documents_uploaded = Column(Boolean, default=False, nullable=False)
    profile_completed = Column(Boolean, default=False, nullable=False)
    menu_uploaded = Column(Boolean, default=False, nullable=False)
    bank_details_added = Column(Boolean, default=False, nullable=False)
    
    # Verification status
    verification_status = Column(String(20), default='pending', nullable=False)  # pending, in_review, approved, rejected
    verification_notes = Column(Text)
    verified_by = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl.user_id'))
    verified_at = Column(TIMESTAMP)
    
    # Document URLs
    fssai_license_url = Column(String(500))
    gst_certificate_url = Column(String(500))
    pan_card_url = Column(String(500))
    bank_proof_url = Column(String(500))
    
    # Business details
    business_type = Column(String(50))  # cloud_kitchen, dine_in, both
    estimated_daily_orders = Column(Integer)
    
    # Timestamps
    started_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    completed_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
