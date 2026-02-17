"""
Restaurant onboarding API endpoints.
Handles restaurant owner registration, onboarding workflow, and document uploads.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app.infra.db.postgres.postgres_config import get_db
from app.api.schemas.onboarding_schemas import (
    RestaurantRegistrationRequest, RestaurantRegistrationResponse,
    OnboardingProgressResponse, DocumentUploadRequest, DocumentUploadResponse,
    RestaurantProfileSetupRequest, RestaurantProfileSetupResponse,
    BankDetailsRequest, BankDetailsResponse,
    BulkMenuUploadRequest, BulkMenuUploadResponse,
    OnboardingSubmitResponse
)
from app.api.schemas.common_schemas import CommonResponse
from app.api.dependencies import get_current_user
from app.infra.db.postgres.models.user import User
from app.infra.db.postgres.models.restaurant import Restaurant
from app.services.onboarding_service import OnboardingService
from app.services.csv_menu_service import CSVMenuService
from app.utils.auth_utils import AuthUtils
from app.utils.enums import UserRole
from app.config.logger import get_logger

router = APIRouter(prefix="/onboarding", tags=["Restaurant Onboarding"])
logger = get_logger(__name__)


@router.post("/register", response_model=CommonResponse[RestaurantRegistrationResponse], status_code=201)
async def register_restaurant_owner(
    request: RestaurantRegistrationRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new restaurant owner and create onboarding record.
    This creates a user with restaurant_owner role and initiates the onboarding process.
    """
    try:
        # Check if user already exists
        existing_user = AuthUtils.get_user_by_email(db, request.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        existing_phone = AuthUtils.get_user_by_phone(db, request.phone)
        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this phone number already exists"
            )
        
        # Create user with restaurant_owner role
        user = AuthUtils.create_user(
            db=db,
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            phone=request.phone,
            password=request.password,
            role=UserRole.RESTAURANT_OWNER.value
        )
        
        # Create onboarding record
        onboarding = OnboardingService.create_onboarding(
            db=db,
            user_id=user.user_id,
            business_type=request.business_type,
            estimated_daily_orders=request.estimated_daily_orders
        )
        
        logger.info(f"Restaurant owner registered: {user.email}, onboarding_id: {onboarding.onboarding_id}")
        
        return CommonResponse(
            code=201,
            message="Restaurant owner registered successfully. Please complete the onboarding process.",
            message_id="REGISTRATION_SUCCESS",
            data=RestaurantRegistrationResponse(
                success=True,
                message="Registration successful",
                user_id=user.user_id,
                onboarding_id=onboarding.onboarding_id,
                email=user.email,
                phone=user.phone
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.get("/status", response_model=CommonResponse[OnboardingProgressResponse])
async def get_onboarding_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current onboarding progress for the authenticated restaurant owner."""
    try:
        # Verify user is restaurant owner
        if current_user.role != UserRole.RESTAURANT_OWNER.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only restaurant owners can access onboarding status"
            )
        
        # Get onboarding record
        onboarding = OnboardingService.get_onboarding_by_user(db, current_user.user_id)
        if not onboarding:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Onboarding record not found"
            )
        
        # Get steps status
        steps_completed = OnboardingService.get_steps_status(onboarding)
        
        return CommonResponse(
            code=200,
            message="Onboarding status retrieved successfully",
            message_id="STATUS_RETRIEVED",
            data=OnboardingProgressResponse(
                onboarding_id=onboarding.onboarding_id,
                user_id=onboarding.user_id,
                restaurant_id=onboarding.restaurant_id,
                current_step=onboarding.current_step,
                completion_percentage=onboarding.completion_percentage,
                verification_status=onboarding.verification_status,
                steps_completed=steps_completed,
                started_at=onboarding.started_at,
                completed_at=onboarding.completed_at
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get onboarding status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve onboarding status: {str(e)}"
        )


@router.post("/documents", response_model=CommonResponse[DocumentUploadResponse])
async def upload_document(
    request: DocumentUploadRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload verification documents (FSSAI, GST, PAN, bank proof)."""
    try:
        # Get onboarding record
        onboarding = OnboardingService.get_onboarding_by_user(db, current_user.user_id)
        if not onboarding:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Onboarding record not found"
            )
        
        # Update document
        updated_onboarding = OnboardingService.update_documents(
            db=db,
            onboarding_id=onboarding.onboarding_id,
            document_type=request.document_type,
            document_url=request.document_url
        )
        
        logger.info(f"Document uploaded: {request.document_type} for onboarding {onboarding.onboarding_id}")
        
        return CommonResponse(
            code=200,
            message=f"{request.document_type.upper()} document uploaded successfully",
            message_id="DOCUMENT_UPLOADED",
            data=DocumentUploadResponse(
                success=True,
                message="Document uploaded successfully",
                document_type=request.document_type,
                document_url=request.document_url,
                documents_uploaded=updated_onboarding.documents_uploaded
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Document upload failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document upload failed: {str(e)}"
        )


@router.put("/profile", response_model=CommonResponse[RestaurantProfileSetupResponse])
async def setup_restaurant_profile(
    request: RestaurantProfileSetupRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Complete restaurant profile setup."""
    try:
        # Get onboarding record
        onboarding = OnboardingService.get_onboarding_by_user(db, current_user.user_id)
        if not onboarding:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Onboarding record not found"
            )
        
        # Check if restaurant already exists
        if onboarding.restaurant_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Restaurant profile already exists"
            )
        
        # Create restaurant record
        restaurant = Restaurant(
            owner_id=current_user.user_id,
            name=onboarding.business_type,  # This should come from registration
            description=request.description,
            phone=current_user.phone,
            email=current_user.email,
            address_line1=request.address_line1,
            address_line2=request.address_line2,
            city=request.city,
            state=request.state,
            postal_code=request.postal_code,
            latitude=request.latitude,
            longitude=request.longitude,
            image=request.image_url,
            cover_image=request.cover_image_url,
            opening_time=request.opening_time,
            closing_time=request.closing_time,
            min_order_amount=request.min_order_amount,
            delivery_fee=request.delivery_fee,
            is_pure_veg=request.is_pure_veg,
            cost_for_two=request.cost_for_two,
            avg_delivery_time=request.avg_delivery_time,
            status='inactive',  # Will be activated after approval
            onboarding_completed=False,
            approval_status='pending'
        )
        
        db.add(restaurant)
        db.commit()
        db.refresh(restaurant)
        
        # Update onboarding record
        updated_onboarding = OnboardingService.complete_profile(
            db=db,
            onboarding_id=onboarding.onboarding_id,
            restaurant_id=restaurant.restaurant_id
        )
        
        logger.info(f"Restaurant profile created: {restaurant.restaurant_id}")
        
        return CommonResponse(
            code=200,
            message="Restaurant profile created successfully",
            message_id="PROFILE_CREATED",
            data=RestaurantProfileSetupResponse(
                success=True,
                message="Profile setup complete",
                restaurant_id=restaurant.restaurant_id,
                profile_completed=updated_onboarding.profile_completed
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Profile setup failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Profile setup failed: {str(e)}"
        )


@router.put("/bank-details", response_model=CommonResponse[BankDetailsResponse])
async def add_bank_details(
    request: BankDetailsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add bank account details for settlements."""
    try:
        # Get onboarding record
        onboarding = OnboardingService.get_onboarding_by_user(db, current_user.user_id)
        if not onboarding or not onboarding.restaurant_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please complete restaurant profile first"
            )
        
        # Update restaurant with bank details
        restaurant = db.query(Restaurant).filter(
            Restaurant.restaurant_id == onboarding.restaurant_id
        ).first()
        
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )
        
        restaurant.bank_account_number = request.account_number
        restaurant.bank_ifsc_code = request.ifsc_code
        restaurant.bank_account_holder_name = request.account_holder_name
        restaurant.bank_name = request.bank_name
        restaurant.fssai_license_number = request.fssai_license_number
        restaurant.gst_number = request.gst_number
        restaurant.pan_number = request.pan_number
        
        # Update onboarding
        updated_onboarding = OnboardingService.complete_bank_details(
            db=db,
            onboarding_id=onboarding.onboarding_id
        )
        
        db.commit()
        
        logger.info(f"Bank details added for restaurant {restaurant.restaurant_id}")
        
        return CommonResponse(
            code=200,
            message="Bank details added successfully",
            message_id="BANK_DETAILS_ADDED",
            data=BankDetailsResponse(
                success=True,
                message="Bank details saved",
                bank_details_added=updated_onboarding.bank_details_added
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Bank details update failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add bank details: {str(e)}"
        )


@router.post("/menu/bulk-upload", response_model=CommonResponse[BulkMenuUploadResponse])
async def bulk_upload_menu(
    request: BulkMenuUploadRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Bulk upload menu items from CSV."""
    try:
        # Get onboarding record
        onboarding = OnboardingService.get_onboarding_by_user(db, current_user.user_id)
        if not onboarding or not onboarding.restaurant_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please complete restaurant profile first"
            )
        
        # Process CSV upload
        result = CSVMenuService.process_csv_upload(
            db=db,
            csv_content=request.csv_data,
            restaurant_id=onboarding.restaurant_id
        )
        
        # Update onboarding if successful
        if result['success'] and result['success_count'] > 0:
            OnboardingService.complete_menu_upload(
                db=db,
                onboarding_id=onboarding.onboarding_id
            )
        
        logger.info(f"Bulk menu upload: {result['success_count']} items created for restaurant {onboarding.restaurant_id}")
        
        return CommonResponse(
            code=200 if result['success'] else 400,
            message=f"Uploaded {result['success_count']} items successfully" if result['success'] else "Upload failed",
            message_id="BULK_UPLOAD_COMPLETE",
            data=BulkMenuUploadResponse(
                success=result['success'],
                message=result.get('message', 'Upload complete'),
                total_rows=result['total_rows'],
                success_count=result['success_count'],
                error_count=result['error_count'],
                errors=result['errors'],
                menu_uploaded=result['success']
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Bulk menu upload failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Bulk upload failed: {str(e)}"
        )


@router.get("/menu/template")
async def download_menu_template():
    """Download CSV template for menu upload."""
    try:
        csv_content = CSVMenuService.generate_csv_template()
        
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=menu_template.csv"
            }
        )
    
    except Exception as e:
        logger.error(f"Template generation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate template: {str(e)}"
        )


@router.post("/submit", response_model=CommonResponse[OnboardingSubmitResponse])
async def submit_onboarding(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit onboarding for admin review."""
    try:
        # Get onboarding record
        onboarding = OnboardingService.get_onboarding_by_user(db, current_user.user_id)
        if not onboarding:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Onboarding record not found"
            )
        
        # Submit for review
        updated_onboarding = OnboardingService.submit_for_review(
            db=db,
            onboarding_id=onboarding.onboarding_id
        )
        
        logger.info(f"Onboarding submitted for review: {onboarding.onboarding_id}")
        
        return CommonResponse(
            code=200,
            message="Onboarding submitted for review successfully",
            message_id="ONBOARDING_SUBMITTED",
            data=OnboardingSubmitResponse(
                success=True,
                message="Your onboarding has been submitted for admin review",
                onboarding_id=updated_onboarding.onboarding_id,
                verification_status=updated_onboarding.verification_status,
                submitted_at=updated_onboarding.updated_at
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
        logger.error(f"Onboarding submission failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Submission failed: {str(e)}"
        )
