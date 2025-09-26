from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, timezone
from typing import Optional
import logging

from app.infra.db.postgres.postgres_config import get_db
from app.api.schemas.auth_schemas import (
    LoginRequest, LoginResponse, SignupRequest, SignupResponse,
    GoogleSigninRequest, GoogleSigninResponse, RefreshTokenRequest, RefreshTokenResponse,
    SendOTPRequest, SendOTPResponse, VerifyOTPRequest, VerifyOTPResponse,
    ForgotPasswordRequest, ResetPasswordRequest, LogoutRequest, LogoutResponse,
    UserSessionsResponse, UserSessionResponse
)
from app.api.schemas.common_schemas import CommonResponse
from app.api.dependencies import get_current_user, get_device_info
from app.utils.auth_utils import AuthUtils
from app.infra.db.postgres.models.user import User
from app.infra.db.postgres.models.refresh_token import RefreshToken
from app.infra.db.postgres.models.oauth_provider import OAuthProvider
from app.infra.db.postgres.models.user_session import UserSession
from app.utils.enums import UserRole, UserStatus
from app.config.config import JWT_EXPIRATION_HOURS

router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = logging.getLogger(__name__)

# Constants
FORGOT_PASSWORD_SUCCESS_MESSAGE = "If the email exists, an OTP has been sent"
OTP_VERIFIED_SUCCESS_MESSAGE = "OTP verified successfully"

@router.post("/login", response_model=CommonResponse[LoginResponse])
async def login(
    request: LoginRequest,
    http_request: Request,
    db: Session = Depends(get_db)
):
    """User login with email and password"""
    try:
        # Get user by email
        user = AuthUtils.get_user_by_email(db, request.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Verify password
        if not AuthUtils.verify_password(request.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Check if user is active
        if user.status != UserStatus.ACTIVE.value:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is not active"
            )
        
        # Generate tokens
        access_token = AuthUtils.generate_jwt_token(str(user.user_id), user.role)
        refresh_token_obj = AuthUtils.create_refresh_token(
            db, str(user.user_id), get_device_info(http_request),
            http_request.client.host if http_request.client else None,
            http_request.headers.get("user-agent")
        )
        
        # Create user session
        AuthUtils.create_user_session(
            db, str(user.user_id), get_device_info(http_request),
            http_request.client.host if http_request.client else None,
            http_request.headers.get("user-agent")
        )
        
        return CommonResponse(
            code=200,
            message="Login successful",
            message_id="LOGIN_SUCCESS",
            data=LoginResponse(
                user=user,
                tokens={
                    "access_token": access_token,
                    "refresh_token": refresh_token_obj.token_hash,  # Return the hash for client
                    "token_type": "bearer",
                    "expires_in": JWT_EXPIRATION_HOURS * 3600
                },
                is_new_user=False,
                requires_verification=not user.email_verified
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@router.post("/signup", response_model=CommonResponse[SignupResponse], status_code=201)
async def signup(
    request: SignupRequest,
    http_request: Request,
    db: Session = Depends(get_db)
):
    """User registration"""
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
        
        # Create new user
        user = AuthUtils.create_user(
            db=db,
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            phone=request.phone,
            password=request.password,
            role=UserRole.CUSTOMER.value
        )
        
        # Generate tokens
        access_token = AuthUtils.generate_jwt_token(str(user.user_id), user.role)
        refresh_token_obj = AuthUtils.create_refresh_token(
            db, str(user.user_id), get_device_info(http_request),
            http_request.client.host if http_request.client else None,
            http_request.headers.get("user-agent")
        )
        
        # Create user session
        AuthUtils.create_user_session(
            db, str(user.user_id), get_device_info(http_request),
            http_request.client.host if http_request.client else None,
            http_request.headers.get("user-agent")
        )
        
        return CommonResponse(
            code=201,
            message="User registered successfully",
            message_id="SIGNUP_SUCCESS",
            data=SignupResponse(
                user=user,
                tokens={
                    "access_token": access_token,
                    "refresh_token": refresh_token_obj.token_hash,
                    "token_type": "bearer",
                    "expires_in": JWT_EXPIRATION_HOURS * 3600
                },
                requires_verification=True
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Signup failed: {str(e)}"
        )

@router.post("/google-signin", response_model=CommonResponse[GoogleSigninResponse])
async def google_signin(
    request: GoogleSigninRequest,
    http_request: Request,
    db: Session = Depends(get_db)
):
    """Google OAuth signin"""
    try:
        # Verify Google token
        google_user_info = await AuthUtils.verify_google_token(request.id_token)
        if not google_user_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Google token"
            )
        
        # Check if user exists by email
        user = AuthUtils.get_user_by_email(db, google_user_info["email"])
        is_new_user = False
        
        if not user:
            # Create new user
            user = AuthUtils.create_user(
                db=db,
                first_name=google_user_info.get("given_name", ""),
                last_name=google_user_info.get("family_name", ""),
                email=google_user_info["email"],
                phone="",  # Google doesn't provide phone
                password=AuthUtils.generate_refresh_token(),  # Random password
                role=UserRole.CUSTOMER.value
            )
            user.email_verified = google_user_info.get("email_verified", False)
            db.commit()
            is_new_user = True
        
        # Create or update OAuth provider record
        oauth_provider = db.query(OAuthProvider).filter(
            OAuthProvider.user_id == user.user_id,
            OAuthProvider.provider == "google"
        ).first()
        
        if not oauth_provider:
            AuthUtils.create_oauth_provider(
                db=db,
                user_id=str(user.user_id),
                provider="google",
                provider_user_id=google_user_info["google_id"],
                provider_email=google_user_info["email"],
                provider_name=google_user_info["name"],
                provider_photo_url=google_user_info.get("picture")
            )
        
        # Generate tokens
        access_token = AuthUtils.generate_jwt_token(str(user.user_id), user.role)
        refresh_token_obj = AuthUtils.create_refresh_token(
            db, str(user.user_id), request.device_info,
            http_request.client.host if http_request.client else None,
            http_request.headers.get("user-agent")
        )
        
        # Create user session
        AuthUtils.create_user_session(
            db, str(user.user_id), request.device_info,
            http_request.client.host if http_request.client else None,
            http_request.headers.get("user-agent")
        )
        
        return CommonResponse(
            code=200,
            message="Google signin successful",
            message_id="GOOGLE_SIGNIN_SUCCESS",
            data=GoogleSigninResponse(
                user=user,
                tokens={
                    "access_token": access_token,
                    "refresh_token": refresh_token_obj.token_hash,
                    "token_type": "bearer",
                    "expires_in": JWT_EXPIRATION_HOURS * 3600
                },
                is_new_user=is_new_user,
                requires_verification=not user.email_verified
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Google signin failed: {str(e)}"
        )

@router.post("/refresh", response_model=CommonResponse[RefreshTokenResponse])
async def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token"""
    try:
        # Find refresh token
        refresh_tokens = db.query(RefreshToken).filter(
            RefreshToken.is_revoked == False
        ).all()
        
        refresh_token_obj = None
        for rt in refresh_tokens:
            if AuthUtils.verify_password(request.refresh_token, rt.token_hash):
                refresh_token_obj = rt
                break
        
        if not refresh_token_obj:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Check if token is expired
        if refresh_token_obj.expires_at < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired"
            )
        
        # Get user
        user = AuthUtils.get_user_by_id(db, str(refresh_token_obj.user_id))
        if not user or user.status != UserStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Generate new tokens
        access_token = AuthUtils.generate_jwt_token(str(user.user_id), user.role)
        new_refresh_token = AuthUtils.generate_refresh_token()
        new_refresh_token_hash = AuthUtils.hash_password(new_refresh_token)
        
        # Update refresh token
        refresh_token_obj.token_hash = new_refresh_token_hash
        refresh_token_obj.expires_at = datetime.now(timezone.utc) + timedelta(days=30)
        db.commit()
        
        return CommonResponse(
            code=200,
            message="Token refreshed successfully",
            message_id="REFRESH_SUCCESS",
            data=RefreshTokenResponse(
                access_token=access_token,
                refresh_token=new_refresh_token,
                token_type="bearer",
                expires_in=JWT_EXPIRATION_HOURS * 3600
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token refresh failed: {str(e)}"
        )

@router.post("/logout", response_model=CommonResponse[LogoutResponse])
async def logout(
    request: LogoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """User logout"""
    try:
        logged_out_count = 0
        
        if request.logout_all_devices:
            # Revoke all refresh tokens for user
            refresh_tokens = db.query(RefreshToken).filter(
                RefreshToken.user_id == current_user.user_id,
                RefreshToken.is_revoked == False
            ).all()
            
            for rt in refresh_tokens:
                rt.is_revoked = True
                logged_out_count += 1
            
            # Deactivate all sessions
            sessions = db.query(UserSession).filter(
                UserSession.user_id == current_user.user_id,
                UserSession.is_active == True
            ).all()
            
            for session in sessions:
                session.is_active = False
                logged_out_count += 1
        
        else:
            # Revoke specific refresh token and deactivate corresponding session
            if request.refresh_token:
                refresh_tokens = db.query(RefreshToken).filter(
                    RefreshToken.user_id == current_user.user_id,
                    RefreshToken.is_revoked == False
                ).all()
                
                for rt in refresh_tokens:
                    if AuthUtils.verify_password(request.refresh_token, rt.token_hash):
                        rt.is_revoked = True
                        logged_out_count = 1
                        
                        # Also deactivate the corresponding session for this device
                        device_info = rt.device_info
                        if device_info and 'device_id' in device_info:
                            session = db.query(UserSession).filter(
                                UserSession.user_id == current_user.user_id,
                                UserSession.device_id == device_info['device_id']
                            ).first()
                            
                            if session:
                                session.is_active = False
                                logged_out_count += 1
                        break
        
        db.commit()
        
        return CommonResponse(
            code=200,
            message="Logout successful",
            message_id="LOGOUT_SUCCESS",
            data=LogoutResponse(
                message="Logged out successfully",
                logged_out_devices=logged_out_count
            )
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Logout failed: {str(e)}"
        )

@router.get("/sessions", response_model=CommonResponse[UserSessionsResponse])
async def get_user_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's active sessions"""
    try:
        sessions = db.query(UserSession).filter(
            UserSession.user_id == current_user.user_id,
            UserSession.is_active == True
        ).order_by(UserSession.last_activity.desc()).all()
        
        session_responses = []
        for session in sessions:
            session_responses.append(UserSessionResponse(
                session_id=session.session_id,
                device_name=session.device_name,
                device_type=session.device_type,
                platform=session.platform,
                app_version=session.app_version,
                last_activity=session.last_activity,
                is_current=False  # You can implement logic to identify current session
            ))
        
        return CommonResponse(
            code=200,
            message="Sessions retrieved successfully",
            message_id="SESSIONS_RETRIEVED",
            data=UserSessionsResponse(
                sessions=session_responses,
                total_sessions=len(session_responses)
            )
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve sessions: {str(e)}"
        )

@router.post("/forgot-password", response_model=CommonResponse[SendOTPResponse])
async def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    """Send OTP for password reset"""
    try:
        from app.utils.otp_utils import OTPUtils
        from app.services.email_service import email_service
        
        # Check if user exists
        user = AuthUtils.get_user_by_email(db, request.email)
        if not user:
            # For security, don't reveal if email exists or not
            return CommonResponse(
                code=200,
                message=FORGOT_PASSWORD_SUCCESS_MESSAGE,
                message_id="FORGOT_PASSWORD_SUCCESS",
                data=SendOTPResponse(
                    message=FORGOT_PASSWORD_SUCCESS_MESSAGE,
                    expires_in=600,  # 10 minutes
                    email=request.email
                )
            )
        
        # Check if user is active
        if user.status != UserStatus.ACTIVE.value:
            return CommonResponse(
                code=200,
                message=FORGOT_PASSWORD_SUCCESS_MESSAGE,
                message_id="FORGOT_PASSWORD_SUCCESS",
                data=SendOTPResponse(
                    message=FORGOT_PASSWORD_SUCCESS_MESSAGE,
                    expires_in=600,
                    email=request.email
                )
            )
        
        # Create OTP record for password reset
        otp_record = OTPUtils.create_otp_record(
            db=db,
            user_id=str(user.user_id),
            email=request.email,
            otp_type="password_reset"
        )
        
        if not otp_record:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate OTP"
            )
        
        # Send OTP email
        email_sent = await email_service.send_otp_email(
            to_email=request.email,
            otp_code=otp_record.otp_code,
            user_name=f"{user.first_name} {user.last_name}".strip(),
            otp_type="password_reset"
        )
        
        if not email_sent:
            # If email fails, still return success for security
            logger.warning(f"Failed to send OTP email to {request.email}")
        
        return CommonResponse(
            code=200,
            message=FORGOT_PASSWORD_SUCCESS_MESSAGE,
            message_id="FORGOT_PASSWORD_SUCCESS",
            data=SendOTPResponse(
                message=FORGOT_PASSWORD_SUCCESS_MESSAGE,
                expires_in=600,
                email=request.email
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Forgot password failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process forgot password request"
        )

@router.post("/verify-reset-otp", response_model=CommonResponse[VerifyOTPResponse])
async def verify_reset_otp(
    request: VerifyOTPRequest,
    db: Session = Depends(get_db)
):
    """Verify OTP for password reset"""
    try:
        from app.utils.otp_utils import OTPUtils
        
        # Verify OTP
        result = OTPUtils.verify_otp(
            db=db,
            otp_code=request.otp_code,
            email=request.email,
            otp_type="password_reset"
        )
        
        if not result["success"]:
            # Increment attempts for failed verification
            OTPUtils.increment_otp_attempts(
                db=db,
                otp_code=request.otp_code,
                email=request.email,
                otp_type="password_reset"
            )
            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["message"]
            )
        
        return CommonResponse(
            code=200,
            message=OTP_VERIFIED_SUCCESS_MESSAGE,
            message_id="OTP_VERIFY_SUCCESS",
            data=VerifyOTPResponse(
                verified=True,
                message=f"{OTP_VERIFIED_SUCCESS_MESSAGE}. You can now reset your password.",
                requires_profile_completion=False
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"OTP verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to verify OTP"
        )

@router.post("/reset-password", response_model=CommonResponse[dict])
async def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """Reset password after OTP verification"""
    try:
        from app.utils.otp_utils import OTPUtils
        from app.infra.db.postgres.models.otp_verification import OTPVerification
        from sqlalchemy import and_
        
        # Find the verified OTP record
        otp_record = db.query(OTPVerification).filter(
            and_(
                OTPVerification.otp_code == request.otp_code,
                OTPVerification.email == request.email,
                OTPVerification.otp_type == "password_reset",
                OTPVerification.is_verified == True
            )
        ).first()
        
        if not otp_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )
        
        # Check if OTP is still valid (not expired)
        if OTPUtils.is_otp_expired(otp_record.expires_at):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reset token has expired"
            )
        
        # Get user
        user = AuthUtils.get_user_by_id(db, str(otp_record.user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found"
            )
        
        # Update password
        new_password_hash = AuthUtils.hash_password(request.new_password)
        user.password_hash = new_password_hash
        user.updated_at = datetime.now(timezone.utc)
        
        # Mark OTP as used (invalidate it)
        otp_record.is_verified = False  # Mark as used
        otp_record.attempts = otp_record.max_attempts  # Mark as exhausted
        
        db.commit()
        
        # Revoke all existing refresh tokens for security
        refresh_tokens = db.query(RefreshToken).filter(
            RefreshToken.user_id == user.user_id,
            RefreshToken.is_revoked == False
        ).all()
        
        for rt in refresh_tokens:
            rt.is_revoked = True
        
        # Deactivate all user sessions
        sessions = db.query(UserSession).filter(
            UserSession.user_id == user.user_id,
            UserSession.is_active == True
        ).all()
        
        for session in sessions:
            session.is_active = False
        
        db.commit()
        
        logger.info(f"Password reset successfully for user {user.user_id}")
        
        return CommonResponse(
            code=200,
            message="Password reset successfully",
            message_id="PASSWORD_RESET_SUCCESS",
            data={
                "message": "Password has been reset successfully. Please login with your new password.",
                "user_id": str(user.user_id)
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Password reset failed: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reset password"
        )

@router.post("/send-otp", response_model=CommonResponse[SendOTPResponse])
async def send_otp(request: SendOTPRequest, db: Session = Depends(get_db)):
    """Send OTP for verification (email or phone)"""
    try:
        from app.utils.otp_utils import OTPUtils
        from app.services.email_service import email_service
        
        # Validate that either email or phone is provided
        if not request.email and not request.phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either email or phone must be provided"
            )
        
        # Get user by email or phone
        user = None
        if request.email:
            user = AuthUtils.get_user_by_email(db, request.email)
        elif request.phone:
            user = AuthUtils.get_user_by_phone(db, request.phone)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Create OTP record
        otp_record = OTPUtils.create_otp_record(
            db=db,
            user_id=str(user.user_id),
            email=request.email,
            phone=request.phone,
            otp_type=request.otp_type
        )
        
        if not otp_record:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate OTP"
            )
        
        # Send OTP based on type
        if request.email and request.otp_type in ["email_verification", "password_reset"]:
            email_sent = await email_service.send_otp_email(
                to_email=request.email,
                otp_code=otp_record.otp_code,
                user_name=f"{user.first_name} {user.last_name}".strip(),
                otp_type=request.otp_type
            )
            
            if not email_sent:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to send OTP email"
                )
        
        elif request.phone and request.otp_type == "phone_verification":
            # Log OTP for development/testing purposes
            # In production, integrate with SMS service like Twilio or MSG91
            logger.info(f"Phone OTP: {otp_record.otp_code} for {request.phone}")
            # TODO: Implement actual SMS sending service integration
        
        return CommonResponse(
            code=200,
            message="OTP sent successfully",
            message_id="OTP_SENT_SUCCESS",
            data=SendOTPResponse(
                message="OTP sent successfully",
                expires_in=600,  # 10 minutes
                phone=request.phone,
                email=request.email
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Send OTP failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send OTP"
        )

@router.post("/verify-otp", response_model=CommonResponse[VerifyOTPResponse])
async def verify_otp(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    """Verify OTP for email or phone verification"""
    try:
        from app.utils.otp_utils import OTPUtils
        
        # Verify OTP
        result = OTPUtils.verify_otp(
            db=db,
            otp_code=request.otp_code,
            email=request.email,
            phone=request.phone,
            otp_type=request.otp_type
        )
        
        if not result["success"]:
            # Increment attempts for failed verification
            OTPUtils.increment_otp_attempts(
                db=db,
                otp_code=request.otp_code,
                email=request.email,
                phone=request.phone,
                otp_type=request.otp_type
            )
            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["message"]
            )
        
        # Update user verification status based on OTP type
        user_id = result["user_id"]
        user = AuthUtils.get_user_by_id(db, user_id)
        
        if user:
            if request.otp_type == "email_verification":
                user.email_verified = True
            elif request.otp_type == "phone_verification":
                user.phone_verified = True
            
            user.updated_at = datetime.now(timezone.utc)
            db.commit()
        
        return CommonResponse(
            code=200,
            message=OTP_VERIFIED_SUCCESS_MESSAGE,
            message_id="OTP_VERIFY_SUCCESS",
            data=VerifyOTPResponse(
                verified=True,
                message=OTP_VERIFIED_SUCCESS_MESSAGE,
                requires_profile_completion=False
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"OTP verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to verify OTP"
        )
