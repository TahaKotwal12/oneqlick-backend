import traceback
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.infra.db.postgres.postgres_config import get_db
from app.api.schemas.common_schemas import CommonResponse
from app.api.schemas.auth_schemas import (
    LoginRequest, SignupRequest, GoogleSignInRequest, RefreshTokenRequest,
    ForgotPasswordRequest, ResetPasswordRequest, VerifyOTPRequest,
    ResendOTPRequest, ChangePasswordRequest, LogoutRequest,
    LoginResponse, SignupResponse, GoogleSignInResponse, RefreshTokenResponse,
    OTPResponse, VerifyOTPResponse, PasswordResetResponse, LogoutResponse,
    UserSessionsResponse, DeviceInfo
)
from app.domain.services.auth_service import AuthService
from app.config.logger import get_logger

router = APIRouter()

def get_device_info(request: Request) -> Optional[DeviceInfo]:
    """Extract device information from request headers."""
    try:
        headers = request.headers
        return DeviceInfo(
            device_id=headers.get('x-device-id', 'unknown'),
            device_name=headers.get('x-device-name'),
            device_type=headers.get('x-device-type'),
            platform=headers.get('x-platform'),
            app_version=headers.get('x-app-version'),
            ip_address=request.client.host if request.client else None,
            user_agent=headers.get('user-agent')
        )
    except Exception as e:
        logger = get_logger(__name__)
        logger.warning(f"Could not extract device info: {str(e)}")
        return None

@router.post("/auth/login", 
            response_model=CommonResponse[LoginResponse],
            status_code=status.HTTP_200_OK,
            tags=["Authentication"])
async def login(
    login_data: LoginRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Authenticate user with email and password.
    
    Returns JWT access token and refresh token for authenticated user.
    """
    logger = get_logger(__name__)
    try:
        logger.info(f"Processing login request for email: {login_data.email}")
        
        auth_service = AuthService(db)
        device_info = get_device_info(request)
        
        result = auth_service.login(login_data, device_info)
        
        logger.info(f"User {login_data.email} logged in successfully")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Login successful",
            message_id="0",
            data=result
        )
        
    except ValueError as e:
        logger.warning(f"Login validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        error_msg = f"Login error: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login"
        )

@router.post("/auth/signup", 
            response_model=CommonResponse[SignupResponse],
            status_code=status.HTTP_201_CREATED,
            tags=["Authentication"])
async def signup(
    signup_data: SignupRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Register a new user account.
    
    Creates a new user account and sends OTP for phone verification.
    """
    logger = get_logger(__name__)
    try:
        logger.info(f"Processing signup request for email: {signup_data.email}")
        
        auth_service = AuthService(db)
        device_info = get_device_info(request)
        
        result = auth_service.signup(signup_data, device_info)
        
        logger.info(f"User {signup_data.email} registered successfully")
        return CommonResponse(
            code=status.HTTP_201_CREATED,
            message="Account created successfully. Please verify your phone number.",
            message_id="0",
            data=result
        )
        
    except ValueError as e:
        logger.warning(f"Signup validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        error_msg = f"Signup error: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during signup"
        )

@router.post("/auth/google-signin", 
            response_model=CommonResponse[GoogleSignInResponse],
            status_code=status.HTTP_200_OK,
            tags=["Authentication"])
async def google_signin(
    google_data: GoogleSignInRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Authenticate user with Google OAuth.
    
    Verifies Google ID token and creates/links user account.
    """
    logger = get_logger(__name__)
    try:
        logger.info("Processing Google signin request")
        
        auth_service = AuthService(db)
        device_info = get_device_info(request)
        
        result = auth_service.google_signin(google_data, device_info)
        
        logger.info(f"Google signin successful for user: {result.user.email}")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Google signin successful",
            message_id="0",
            data=result
        )
        
    except ValueError as e:
        logger.warning(f"Google signin validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        error_msg = f"Google signin error: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during Google signin"
        )

@router.post("/auth/refresh", 
            response_model=CommonResponse[RefreshTokenResponse],
            status_code=status.HTTP_200_OK,
            tags=["Authentication"])
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    
    Generates new access token and refresh token pair.
    """
    logger = get_logger(__name__)
    try:
        logger.info("Processing token refresh request")
        
        auth_service = AuthService(db)
        result = auth_service.refresh_token(refresh_data)
        
        logger.info("Token refreshed successfully")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Token refreshed successfully",
            message_id="0",
            data=result
        )
        
    except ValueError as e:
        logger.warning(f"Token refresh validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        error_msg = f"Token refresh error: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during token refresh"
        )

@router.post("/auth/send-otp", 
            response_model=CommonResponse[OTPResponse],
            status_code=status.HTTP_200_OK,
            tags=["Authentication"])
async def send_otp(
    otp_data: ResendOTPRequest,
    db: Session = Depends(get_db)
):
    """
    Send OTP for phone or email verification.
    
    Sends OTP to the specified phone number or email address.
    """
    logger = get_logger(__name__)
    try:
        logger.info(f"Processing send OTP request for: {otp_data.phone or otp_data.email}")
        
        auth_service = AuthService(db)
        result = auth_service.send_otp(otp_data.phone, otp_data.email, otp_data.otp_type)
        
        logger.info(f"OTP sent successfully to: {otp_data.phone or otp_data.email}")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="OTP sent successfully",
            message_id="0",
            data=result
        )
        
    except ValueError as e:
        logger.warning(f"Send OTP validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        error_msg = f"Send OTP error: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while sending OTP"
        )

@router.post("/auth/verify-otp", 
            response_model=CommonResponse[VerifyOTPResponse],
            status_code=status.HTTP_200_OK,
            tags=["Authentication"])
async def verify_otp(
    verify_data: VerifyOTPRequest,
    db: Session = Depends(get_db)
):
    """
    Verify OTP code for phone or email verification.
    
    Verifies the OTP code and updates user verification status.
    """
    logger = get_logger(__name__)
    try:
        logger.info(f"Processing OTP verification for: {verify_data.phone or verify_data.email}")
        
        auth_service = AuthService(db)
        result = auth_service.verify_otp(verify_data)
        
        logger.info(f"OTP verified successfully for: {verify_data.phone or verify_data.email}")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="OTP verified successfully",
            message_id="0",
            data=result
        )
        
    except ValueError as e:
        logger.warning(f"OTP verification validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        error_msg = f"OTP verification error: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during OTP verification"
        )

@router.post("/auth/logout", 
            response_model=CommonResponse[LogoutResponse],
            status_code=status.HTTP_200_OK,
            tags=["Authentication"])
async def logout(
    logout_data: LogoutRequest,
    # TODO: Add authentication dependency to get current user
    db: Session = Depends(get_db)
):
    """
    Logout user and revoke tokens.
    
    Revokes refresh tokens and deactivates user sessions.
    """
    logger = get_logger(__name__)
    try:
        logger.info("Processing logout request")
        
        # TODO: Get user_id from authenticated user
        # For now, using a placeholder
        user_id = None  # This should come from JWT token
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        
        auth_service = AuthService(db)
        result = auth_service.logout(user_id, logout_data)
        
        logger.info("User logged out successfully")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Logged out successfully",
            message_id="0",
            data=result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Logout error: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during logout"
        )

@router.get("/auth/sessions", 
            response_model=CommonResponse[UserSessionsResponse],
            status_code=status.HTTP_200_OK,
            tags=["Authentication"])
async def get_user_sessions(
    # TODO: Add authentication dependency to get current user
    db: Session = Depends(get_db)
):
    """
    Get all active sessions for the current user.
    
    Returns list of all active sessions across devices.
    """
    logger = get_logger(__name__)
    try:
        logger.info("Processing get user sessions request")
        
        # TODO: Get user_id from authenticated user
        # For now, using a placeholder
        user_id = None  # This should come from JWT token
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        
        auth_service = AuthService(db)
        result = auth_service.get_user_sessions(user_id)
        
        logger.info(f"Retrieved {result.total_sessions} sessions for user")
        return CommonResponse(
            code=status.HTTP_200_OK,
            message="Sessions retrieved successfully",
            message_id="0",
            data=result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Get user sessions error: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving sessions"
        )
