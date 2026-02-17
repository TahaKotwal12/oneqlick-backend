"""
Onboarding service for restaurant owner onboarding workflow.
Handles progress tracking, step completion, and verification status.
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, Dict
from uuid import UUID
from datetime import datetime, timezone

from app.infra.db.postgres.models.restaurant_onboarding import RestaurantOnboarding
from app.infra.db.postgres.models.restaurant import Restaurant
from app.infra.db.postgres.models.user import User
from app.utils.enums import OnboardingStep, OnboardingStatus
from app.config.logger import get_logger

logger = get_logger(__name__)


class OnboardingService:
    """Service for managing restaurant onboarding workflow."""
    
    @staticmethod
    def create_onboarding(
        db: Session,
        user_id: UUID,
        business_type: str,
        estimated_daily_orders: Optional[int] = None
    ) -> RestaurantOnboarding:
        """
        Create a new onboarding record for a restaurant owner.
        
        Args:
            db: Database session
            user_id: User ID of the restaurant owner
            business_type: Type of business (cloud_kitchen, dine_in, both)
            estimated_daily_orders: Estimated daily order volume
            
        Returns:
            RestaurantOnboarding: Created onboarding record
        """
        onboarding = RestaurantOnboarding(
            user_id=user_id,
            business_type=business_type,
            estimated_daily_orders=estimated_daily_orders,
            current_step=OnboardingStep.REGISTRATION.value,
            registration_completed=True,  # Registration is done when this is created
            completion_percentage=20  # 1 of 5 steps done
        )
        
        db.add(onboarding)
        db.commit()
        db.refresh(onboarding)
        
        logger.info(f"Created onboarding record {onboarding.onboarding_id} for user {user_id}")
        return onboarding
    
    @staticmethod
    def get_onboarding_by_user(db: Session, user_id: UUID) -> Optional[RestaurantOnboarding]:
        """Get onboarding record for a user."""
        return db.query(RestaurantOnboarding).filter(
            RestaurantOnboarding.user_id == user_id
        ).first()
    
    @staticmethod
    def get_onboarding_by_id(db: Session, onboarding_id: UUID) -> Optional[RestaurantOnboarding]:
        """Get onboarding record by ID."""
        return db.query(RestaurantOnboarding).filter(
            RestaurantOnboarding.onboarding_id == onboarding_id
        ).first()
    
    @staticmethod
    def update_documents(
        db: Session,
        onboarding_id: UUID,
        document_type: str,
        document_url: str
    ) -> RestaurantOnboarding:
        """
        Update document URL for onboarding.
        
        Args:
            db: Database session
            onboarding_id: Onboarding record ID
            document_type: Type of document (fssai, gst, pan, bank_proof)
            document_url: URL of the uploaded document
            
        Returns:
            RestaurantOnboarding: Updated onboarding record
        """
        onboarding = OnboardingService.get_onboarding_by_id(db, onboarding_id)
        if not onboarding:
            raise ValueError(f"Onboarding record {onboarding_id} not found")
        
        # Update the appropriate document URL
        if document_type == 'fssai':
            onboarding.fssai_license_url = document_url
        elif document_type == 'gst':
            onboarding.gst_certificate_url = document_url
        elif document_type == 'pan':
            onboarding.pan_card_url = document_url
        elif document_type == 'bank_proof':
            onboarding.bank_proof_url = document_url
        
        # Check if all required documents are uploaded
        all_docs_uploaded = all([
            onboarding.fssai_license_url,
            onboarding.gst_certificate_url,
            onboarding.pan_card_url
        ])
        
        if all_docs_uploaded and not onboarding.documents_uploaded:
            onboarding.documents_uploaded = True
            onboarding.current_step = OnboardingStep.PROFILE.value
            logger.info(f"All documents uploaded for onboarding {onboarding_id}")
        
        # Recalculate completion percentage
        onboarding.completion_percentage = OnboardingService.calculate_completion_percentage(onboarding)
        
        db.commit()
        db.refresh(onboarding)
        
        return onboarding
    
    @staticmethod
    def complete_profile(
        db: Session,
        onboarding_id: UUID,
        restaurant_id: UUID
    ) -> RestaurantOnboarding:
        """
        Mark profile setup as completed.
        
        Args:
            db: Database session
            onboarding_id: Onboarding record ID
            restaurant_id: Created restaurant ID
            
        Returns:
            RestaurantOnboarding: Updated onboarding record
        """
        onboarding = OnboardingService.get_onboarding_by_id(db, onboarding_id)
        if not onboarding:
            raise ValueError(f"Onboarding record {onboarding_id} not found")
        
        onboarding.restaurant_id = restaurant_id
        onboarding.profile_completed = True
        onboarding.current_step = OnboardingStep.MENU.value
        onboarding.completion_percentage = OnboardingService.calculate_completion_percentage(onboarding)
        
        db.commit()
        db.refresh(onboarding)
        
        logger.info(f"Profile completed for onboarding {onboarding_id}")
        return onboarding
    
    @staticmethod
    def complete_menu_upload(
        db: Session,
        onboarding_id: UUID
    ) -> RestaurantOnboarding:
        """Mark menu upload as completed."""
        onboarding = OnboardingService.get_onboarding_by_id(db, onboarding_id)
        if not onboarding:
            raise ValueError(f"Onboarding record {onboarding_id} not found")
        
        onboarding.menu_uploaded = True
        onboarding.current_step = OnboardingStep.BANK_DETAILS.value
        onboarding.completion_percentage = OnboardingService.calculate_completion_percentage(onboarding)
        
        db.commit()
        db.refresh(onboarding)
        
        logger.info(f"Menu uploaded for onboarding {onboarding_id}")
        return onboarding
    
    @staticmethod
    def complete_bank_details(
        db: Session,
        onboarding_id: UUID
    ) -> RestaurantOnboarding:
        """Mark bank details as completed."""
        onboarding = OnboardingService.get_onboarding_by_id(db, onboarding_id)
        if not onboarding:
            raise ValueError(f"Onboarding record {onboarding_id} not found")
        
        onboarding.bank_details_added = True
        onboarding.current_step = OnboardingStep.REVIEW.value
        onboarding.completion_percentage = OnboardingService.calculate_completion_percentage(onboarding)
        
        db.commit()
        db.refresh(onboarding)
        
        logger.info(f"Bank details added for onboarding {onboarding_id}")
        return onboarding
    
    @staticmethod
    def submit_for_review(
        db: Session,
        onboarding_id: UUID
    ) -> RestaurantOnboarding:
        """
        Submit onboarding for admin review.
        
        Args:
            db: Database session
            onboarding_id: Onboarding record ID
            
        Returns:
            RestaurantOnboarding: Updated onboarding record
        """
        onboarding = OnboardingService.get_onboarding_by_id(db, onboarding_id)
        if not onboarding:
            raise ValueError(f"Onboarding record {onboarding_id} not found")
        
        # Validate all steps are completed
        if not all([
            onboarding.registration_completed,
            onboarding.documents_uploaded,
            onboarding.profile_completed,
            onboarding.menu_uploaded,
            onboarding.bank_details_added
        ]):
            raise ValueError("Cannot submit incomplete onboarding for review")
        
        onboarding.verification_status = OnboardingStatus.IN_REVIEW.value
        onboarding.current_step = OnboardingStep.REVIEW.value
        onboarding.completion_percentage = 100
        
        db.commit()
        db.refresh(onboarding)
        
        logger.info(f"Onboarding {onboarding_id} submitted for review")
        return onboarding
    
    @staticmethod
    def approve_onboarding(
        db: Session,
        onboarding_id: UUID,
        admin_id: UUID,
        notes: Optional[str] = None
    ) -> RestaurantOnboarding:
        """
        Approve restaurant onboarding.
        
        Args:
            db: Database session
            onboarding_id: Onboarding record ID
            admin_id: Admin user ID who approved
            notes: Optional approval notes
            
        Returns:
            RestaurantOnboarding: Updated onboarding record
        """
        onboarding = OnboardingService.get_onboarding_by_id(db, onboarding_id)
        if not onboarding:
            raise ValueError(f"Onboarding record {onboarding_id} not found")
        
        if not onboarding.restaurant_id:
            raise ValueError("Cannot approve onboarding without restaurant profile")
        
        # Update onboarding status
        onboarding.verification_status = OnboardingStatus.APPROVED.value
        onboarding.verified_by = admin_id
        onboarding.verified_at = datetime.now(timezone.utc)
        onboarding.verification_notes = notes
        onboarding.current_step = OnboardingStep.COMPLETED.value
        onboarding.completed_at = datetime.now(timezone.utc)
        
        # Update restaurant status
        restaurant = db.query(Restaurant).filter(
            Restaurant.restaurant_id == onboarding.restaurant_id
        ).first()
        
        if restaurant:
            restaurant.onboarding_completed = True
            restaurant.approval_status = 'approved'
            restaurant.approved_by = admin_id
            restaurant.approved_at = datetime.now(timezone.utc)
            restaurant.status = 'active'
        
        db.commit()
        db.refresh(onboarding)
        
        logger.info(f"Onboarding {onboarding_id} approved by admin {admin_id}")
        return onboarding
    
    @staticmethod
    def reject_onboarding(
        db: Session,
        onboarding_id: UUID,
        admin_id: UUID,
        reason: str
    ) -> RestaurantOnboarding:
        """
        Reject restaurant onboarding.
        
        Args:
            db: Database session
            onboarding_id: Onboarding record ID
            admin_id: Admin user ID who rejected
            reason: Rejection reason
            
        Returns:
            RestaurantOnboarding: Updated onboarding record
        """
        onboarding = OnboardingService.get_onboarding_by_id(db, onboarding_id)
        if not onboarding:
            raise ValueError(f"Onboarding record {onboarding_id} not found")
        
        onboarding.verification_status = OnboardingStatus.REJECTED.value
        onboarding.verified_by = admin_id
        onboarding.verified_at = datetime.now(timezone.utc)
        onboarding.verification_notes = reason
        
        # Update restaurant status if exists
        if onboarding.restaurant_id:
            restaurant = db.query(Restaurant).filter(
                Restaurant.restaurant_id == onboarding.restaurant_id
            ).first()
            
            if restaurant:
                restaurant.approval_status = 'rejected'
                restaurant.rejection_reason = reason
                restaurant.status = 'inactive'
        
        db.commit()
        db.refresh(onboarding)
        
        logger.info(f"Onboarding {onboarding_id} rejected by admin {admin_id}")
        return onboarding
    
    @staticmethod
    def calculate_completion_percentage(onboarding: RestaurantOnboarding) -> int:
        """
        Calculate completion percentage based on completed steps.
        
        Args:
            onboarding: Onboarding record
            
        Returns:
            int: Completion percentage (0-100)
        """
        steps = [
            onboarding.registration_completed,
            onboarding.documents_uploaded,
            onboarding.profile_completed,
            onboarding.menu_uploaded,
            onboarding.bank_details_added
        ]
        
        completed_count = sum(steps)
        total_steps = len(steps)
        
        return int((completed_count / total_steps) * 100)
    
    @staticmethod
    def get_steps_status(onboarding: RestaurantOnboarding) -> Dict[str, bool]:
        """
        Get status of all onboarding steps.
        
        Args:
            onboarding: Onboarding record
            
        Returns:
            Dict[str, bool]: Dictionary of step names and completion status
        """
        return {
            'registration': onboarding.registration_completed,
            'documents': onboarding.documents_uploaded,
            'profile': onboarding.profile_completed,
            'menu': onboarding.menu_uploaded,
            'bank_details': onboarding.bank_details_added
        }
    
    @staticmethod
    def get_pending_onboardings(db: Session, limit: int = 50, offset: int = 0):
        """Get all pending onboarding requests for admin review."""
        return db.query(RestaurantOnboarding).filter(
            RestaurantOnboarding.verification_status.in_([
                OnboardingStatus.PENDING.value,
                OnboardingStatus.IN_REVIEW.value
            ])
        ).order_by(RestaurantOnboarding.created_at.desc()).limit(limit).offset(offset).all()
