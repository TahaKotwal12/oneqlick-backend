"""
Admin endpoints for restaurant onboarding review and approval.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.infra.db.postgres.postgres_config import get_db
from app.api.schemas.onboarding_schemas import (
    OnboardingDetailResponse, PendingOnboardingListResponse,
    OnboardingApprovalRequest, OnboardingRejectionRequest,
    OnboardingSubmitResponse
)
from app.api.schemas.common_schemas import CommonResponse
from app.api.dependencies import get_current_user, require_admin
from app.infra.db.postgres.models.user import User
from app.services.onboarding_service import OnboardingService
from app.config.logger import get_logger

router = APIRouter(prefix="/admin/onboarding", tags=["Admin - Onboarding"])
logger = get_logger(__name__)


@router.get("/pending", response_model=CommonResponse[PendingOnboardingListResponse])
async def get_pending_onboardings(
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get all pending onboarding requests for admin review."""
    try:
        # Get pending onboardings
        onboardings = OnboardingService.get_pending_onboardings(db, limit, offset)
        
        # Build detailed responses
        onboarding_details = []
        for onboarding in onboardings:
            # Get user info
            user = db.query(User).filter(User.user_id == onboarding.user_id).first()
            if not user:
                continue
            
            # Get restaurant info if exists
            restaurant_name = "Not set"
            cuisine_type = onboarding.business_type or "Not set"
            
            if onboarding.restaurant_id:
                from app.infra.db.postgres.models.restaurant import Restaurant
                restaurant = db.query(Restaurant).filter(
                    Restaurant.restaurant_id == onboarding.restaurant_id
                ).first()
                if restaurant:
                    restaurant_name = restaurant.name
                    cuisine_type = restaurant.cuisine_type or cuisine_type
            
            onboarding_details.append(OnboardingDetailResponse(
                onboarding_id=onboarding.onboarding_id,
                user_id=onboarding.user_id,
                restaurant_id=onboarding.restaurant_id,
                owner_name=f"{user.first_name} {user.last_name}",
                email=user.email,
                phone=user.phone,
                restaurant_name=restaurant_name,
                business_type=onboarding.business_type or "Not set",
                cuisine_type=cuisine_type,
                current_step=onboarding.current_step,
                completion_percentage=onboarding.completion_percentage,
                verification_status=onboarding.verification_status,
                fssai_license_url=onboarding.fssai_license_url,
                gst_certificate_url=onboarding.gst_certificate_url,
                pan_card_url=onboarding.pan_card_url,
                bank_proof_url=onboarding.bank_proof_url,
                fssai_license_number=None,  # Will be in restaurant table
                gst_number=None,
                pan_number=None,
                bank_account_number=None,
                bank_ifsc_code=None,
                bank_account_holder_name=None,
                bank_name=None,
                started_at=onboarding.started_at,
                completed_at=onboarding.completed_at,
                verified_at=onboarding.verified_at
            ))
        
        # Count by status
        pending_count = sum(1 for o in onboardings if o.verification_status == 'pending')
        in_review_count = sum(1 for o in onboardings if o.verification_status == 'in_review')
        
        return CommonResponse(
            code=200,
            message=f"Retrieved {len(onboarding_details)} pending onboardings",
            message_id="PENDING_ONBOARDINGS_RETRIEVED",
            data=PendingOnboardingListResponse(
                total_count=len(onboarding_details),
                pending_count=pending_count,
                in_review_count=in_review_count,
                onboardings=onboarding_details
            )
        )
    
    except Exception as e:
        logger.error(f"Failed to get pending onboardings: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve pending onboardings: {str(e)}"
        )


@router.get("/{onboarding_id}", response_model=CommonResponse[OnboardingDetailResponse])
async def get_onboarding_detail(
    onboarding_id: UUID,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific onboarding request."""
    try:
        onboarding = OnboardingService.get_onboarding_by_id(db, onboarding_id)
        if not onboarding:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Onboarding record not found"
            )
        
        # Get user info
        user = db.query(User).filter(User.user_id == onboarding.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get restaurant info
        restaurant_name = "Not set"
        cuisine_type = onboarding.business_type or "Not set"
        fssai = None
        gst = None
        pan = None
        bank_acc = None
        bank_ifsc = None
        bank_holder = None
        bank_name_val = None
        
        if onboarding.restaurant_id:
            from app.infra.db.postgres.models.restaurant import Restaurant
            restaurant = db.query(Restaurant).filter(
                Restaurant.restaurant_id == onboarding.restaurant_id
            ).first()
            if restaurant:
                restaurant_name = restaurant.name
                cuisine_type = restaurant.cuisine_type or cuisine_type
                fssai = restaurant.fssai_license_number
                gst = restaurant.gst_number
                pan = restaurant.pan_number
                bank_acc = restaurant.bank_account_number
                bank_ifsc = restaurant.bank_ifsc_code
                bank_holder = restaurant.bank_account_holder_name
                bank_name_val = restaurant.bank_name
        
        return CommonResponse(
            code=200,
            message="Onboarding details retrieved successfully",
            message_id="ONBOARDING_DETAIL_RETRIEVED",
            data=OnboardingDetailResponse(
                onboarding_id=onboarding.onboarding_id,
                user_id=onboarding.user_id,
                restaurant_id=onboarding.restaurant_id,
                owner_name=f"{user.first_name} {user.last_name}",
                email=user.email,
                phone=user.phone,
                restaurant_name=restaurant_name,
                business_type=onboarding.business_type or "Not set",
                cuisine_type=cuisine_type,
                current_step=onboarding.current_step,
                completion_percentage=onboarding.completion_percentage,
                verification_status=onboarding.verification_status,
                fssai_license_url=onboarding.fssai_license_url,
                gst_certificate_url=onboarding.gst_certificate_url,
                pan_card_url=onboarding.pan_card_url,
                bank_proof_url=onboarding.bank_proof_url,
                fssai_license_number=fssai,
                gst_number=gst,
                pan_number=pan,
                bank_account_number=bank_acc,
                bank_ifsc_code=bank_ifsc,
                bank_account_holder_name=bank_holder,
                bank_name=bank_name_val,
                started_at=onboarding.started_at,
                completed_at=onboarding.completed_at,
                verified_at=onboarding.verified_at
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get onboarding detail: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve onboarding details: {str(e)}"
        )


@router.post("/{onboarding_id}/approve", response_model=CommonResponse[OnboardingSubmitResponse])
async def approve_onboarding(
    onboarding_id: UUID,
    request: OnboardingApprovalRequest,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Approve a restaurant onboarding request."""
    try:
        # Approve onboarding
        approved_onboarding = OnboardingService.approve_onboarding(
            db=db,
            onboarding_id=onboarding_id,
            admin_id=current_user.user_id,
            notes=request.notes
        )
        
        logger.info(f"Onboarding {onboarding_id} approved by admin {current_user.user_id}")
        
        # TODO: Send approval email to restaurant owner
        
        return CommonResponse(
            code=200,
            message="Onboarding approved successfully",
            message_id="ONBOARDING_APPROVED",
            data=OnboardingSubmitResponse(
                success=True,
                message="Restaurant onboarding has been approved",
                onboarding_id=approved_onboarding.onboarding_id,
                verification_status=approved_onboarding.verification_status,
                submitted_at=approved_onboarding.verified_at
            )
        )
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Onboarding approval failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Approval failed: {str(e)}"
        )


@router.post("/{onboarding_id}/reject", response_model=CommonResponse[OnboardingSubmitResponse])
async def reject_onboarding(
    onboarding_id: UUID,
    request: OnboardingRejectionRequest,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Reject a restaurant onboarding request."""
    try:
        # Reject onboarding
        rejected_onboarding = OnboardingService.reject_onboarding(
            db=db,
            onboarding_id=onboarding_id,
            admin_id=current_user.user_id,
            reason=request.reason
        )
        
        logger.info(f"Onboarding {onboarding_id} rejected by admin {current_user.user_id}")
        
        # TODO: Send rejection email to restaurant owner
        
        return CommonResponse(
            code=200,
            message="Onboarding rejected",
            message_id="ONBOARDING_REJECTED",
            data=OnboardingSubmitResponse(
                success=False,
                message=f"Onboarding rejected: {request.reason}",
                onboarding_id=rejected_onboarding.onboarding_id,
                verification_status=rejected_onboarding.verification_status,
                submitted_at=rejected_onboarding.verified_at
            )
        )
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Onboarding rejection failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Rejection failed: {str(e)}"
        )
