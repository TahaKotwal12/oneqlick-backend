import traceback
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.infra.db.postgres.postgres_config import get_db
from app.infra.redis.redis_config import get_redis_client
from app.api.schemas.common_schemas import CommonResponse
from app.api.schemas.otp_schema import (
    OTPRequestSchema, OTPVerifySchema, OTPResponseSchema, OTPVerifyResponseSchema
)
from app.domain.services.otp_service import OTPService
from app.domain.services.sms_service import SMSService
from app.domain.services.user_service import UserService
from app.config.logger import get_logger

router = APIRouter()

def get_otp_service():
    """Dependency to get OTP service instance."""
    redis_client = get_redis_client()
    return OTPService(redis_client)

def get_sms_service():
    """Dependency to get SMS service instance."""
    return SMSService()

@router.post("/otp/request", 
            response_model=CommonResponse[OTPResponseSchema],
            tags=["OTP"])
async def request_otp(
    otp_request: OTPRequestSchema,
    otp_service: OTPService = Depends(get_otp_service),
    sms_service: SMSService = Depends(get_sms_service),
    db: Session = Depends(get_db),
):
    """
    Request OTP for phone number verification.
    
    This endpoint sends an OTP to the specified phone number for verification.
    Rate limited to 1 request per minute per phone number.
    """
    logger = get_logger(__name__)
    try:
        logger.info(f"Processing OTP request for phone: {otp_request.phone}")
        
        # Validate phone number format
        if not sms_service.validate_phone_number(otp_request.phone):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid phone number format"
            )
        
        # Check if OTP request is allowed (rate limiting)
        is_allowed, message = otp_service.is_otp_request_allowed(otp_request.phone)
        if not is_allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=message
            )
        
        # Generate OTP
        otp = otp_service.generate_otp()
        
        # Store OTP in Redis
        if not otp_service.store_otp(otp_request.phone, otp):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to store OTP"
            )
        
        # Send SMS
        sms_success, sms_message = sms_service.send_otp_sms(otp_request.phone, otp)
        if not sms_success:
            # If SMS fails, delete the stored OTP
            otp_service.delete_otp(otp_request.phone)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to send SMS: {sms_message}"
            )
        
        # Record OTP request for rate limiting
        otp_service.record_otp_request(otp_request.phone)
        
        logger.info(f"OTP sent successfully to {otp_request.phone}")
        
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="OTP sent successfully",
            message_id="0",
            data=OTPResponseSchema(
                success=True,
                message="OTP sent successfully",
                phone=otp_request.phone,
                expires_in_minutes=5,
                attempts_remaining=3
            )
        )
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error in request_otp: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while requesting OTP"
        )

@router.post("/otp/verify", 
            response_model=CommonResponse[OTPVerifyResponseSchema],
            tags=["OTP"])
async def verify_otp(
    otp_verify: OTPVerifySchema,
    otp_service: OTPService = Depends(get_otp_service),
    db: Session = Depends(get_db),
):
    """
    Verify OTP for phone number.
    
    This endpoint verifies the OTP sent to the phone number.
    Maximum 3 attempts allowed per OTP.
    """
    logger = get_logger(__name__)
    try:
        logger.info(f"Processing OTP verification for phone: {otp_verify.phone}")
        
        # Verify OTP
        is_valid, message = otp_service.verify_otp(otp_verify.phone, otp_verify.otp)
        
        if is_valid:
            # If OTP is valid, mark user's phone as verified (if user exists)
            user_service = UserService(db)
            user = user_service.get_user_by_phone(otp_verify.phone)
            if user:
                user_service.verify_user_phone(user.user_id)
                logger.info(f"Phone verified for user: {user.user_id}")
        
        logger.info(f"OTP verification result for {otp_verify.phone}: {is_valid}")
        
        return CommonResponse(
            code=status.HTTP_200_OK,
            message=message,
            message_id="0",
            data=OTPVerifyResponseSchema(
                success=is_valid,
                message=message,
                phone=otp_verify.phone,
                verified=is_valid
            )
        )
        
    except Exception as e:
        error_msg = f"Error in verify_otp: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while verifying OTP"
        )

@router.post("/otp/verify-user/{user_id}", 
            response_model=CommonResponse[OTPVerifyResponseSchema],
            tags=["OTP"])
async def verify_otp_for_user(
    user_id: str,
    otp_verify: OTPVerifySchema,
    otp_service: OTPService = Depends(get_otp_service),
    db: Session = Depends(get_db),
):
    """
    Verify OTP for a specific user.
    
    This endpoint verifies the OTP and marks the user's phone as verified.
    """
    logger = get_logger(__name__)
    try:
        logger.info(f"Processing OTP verification for user: {user_id}, phone: {otp_verify.phone}")
        
        # Verify OTP
        is_valid, message = otp_service.verify_otp(otp_verify.phone, otp_verify.otp)
        
        if is_valid:
            # Mark user's phone as verified
            user_service = UserService(db)
            user = user_service.get_user_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            if user.phone != otp_verify.phone:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Phone number does not match user's phone"
                )
            
            user_service.verify_user_phone(user_id)
            logger.info(f"Phone verified for user: {user_id}")
        
        logger.info(f"OTP verification result for user {user_id}: {is_valid}")
        
        return CommonResponse(
            code=status.HTTP_200_OK,
            message=message,
            message_id="0",
            data=OTPVerifyResponseSchema(
                success=is_valid,
                message=message,
                phone=otp_verify.phone,
                verified=is_valid
            )
        )
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error in verify_otp_for_user: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while verifying OTP"
        ) 