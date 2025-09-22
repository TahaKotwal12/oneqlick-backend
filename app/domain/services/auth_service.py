import jwt
import bcrypt
import secrets
import httpx
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
from uuid import UUID
from sqlalchemy.orm import Session

from app.infra.db.postgres.models.user import User, UserRole, UserStatus
from app.infra.db.postgres.models.auth_models import (
    RefreshToken, OAuthProvider, OTPVerification, UserSession, PasswordResetToken,
    AuthProvider, OTPType, DeviceType, Platform
)
from app.api.schemas.auth_schemas import (
    LoginRequest, SignupRequest, GoogleSignInRequest, RefreshTokenRequest,
    ForgotPasswordRequest, ResetPasswordRequest, VerifyOTPRequest,
    ResendOTPRequest, ChangePasswordRequest, LogoutRequest,
    LoginResponse, SignupResponse, GoogleSignInResponse, RefreshTokenResponse,
    OTPResponse, VerifyOTPResponse, PasswordResetResponse, LogoutResponse,
    UserSessionsResponse, TokenData, DeviceInfo, OTPData, GoogleUserInfo
)
from app.config.config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_HOURS
from app.config.logger import get_logger

logger = get_logger(__name__)

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.jwt_secret = JWT_SECRET_KEY
        self.jwt_algorithm = JWT_ALGORITHM
        self.jwt_expiration_hours = JWT_EXPIRATION_HOURS

    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt with salt."""
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        return password_hash.decode('utf-8')

    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against bcrypt hash."""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        except Exception as e:
            logger.error(f"Error verifying password: {str(e)}")
            return False

    def _generate_tokens(self, user: User, device_info: Optional[DeviceInfo] = None) -> Tuple[str, str]:
        """Generate JWT access token and refresh token."""
        now = datetime.utcnow()
        
        # Create session
        session_id = UUID(int=secrets.randbits(128))
        if device_info:
            session = UserSession(
                session_id=session_id,
                user_id=user.user_id,
                device_id=device_info.device_id,
                device_name=device_info.device_name,
                device_type=DeviceType(device_info.device_type) if device_info.device_type else None,
                platform=Platform(device_info.platform) if device_info.platform else None,
                app_version=device_info.app_version,
                is_active=True
            )
            self.db.add(session)
            self.db.commit()

        # Access token payload
        access_token_payload = {
            'user_id': str(user.user_id),
            'email': user.email,
            'role': user.role.value,
            'session_id': str(session_id),
            'iat': now,
            'exp': now + timedelta(hours=self.jwt_expiration_hours),
            'type': 'access'
        }

        # Generate access token
        access_token = jwt.encode(access_token_payload, self.jwt_secret, algorithm=self.jwt_algorithm)

        # Generate refresh token
        refresh_token = secrets.token_urlsafe(64)
        refresh_token_hash = self._hash_password(refresh_token)
        
        # Store refresh token
        refresh_token_obj = RefreshToken(
            user_id=user.user_id,
            token_hash=refresh_token_hash,
            expires_at=now + timedelta(days=30),  # Refresh token valid for 30 days
            device_info=device_info.dict() if device_info else None,
            ip_address=device_info.ip_address if device_info else None,
            user_agent=device_info.user_agent if device_info else None
        )
        self.db.add(refresh_token_obj)
        self.db.commit()

        return access_token, refresh_token

    def _verify_google_token(self, id_token: str) -> Optional[GoogleUserInfo]:
        """Verify Google ID token and extract user information."""
        try:
            # In production, you should verify the token with Google's servers
            # For now, we'll decode it (in production, use Google's verification)
            decoded_token = jwt.decode(id_token, options={"verify_signature": False})
            
            return GoogleUserInfo(
                google_id=decoded_token.get('sub'),
                email=decoded_token.get('email'),
                name=decoded_token.get('name'),
                given_name=decoded_token.get('given_name'),
                family_name=decoded_token.get('family_name'),
                picture=decoded_token.get('picture'),
                verified_email=decoded_token.get('email_verified', False)
            )
        except Exception as e:
            logger.error(f"Error verifying Google token: {str(e)}")
            return None

    def login(self, login_data: LoginRequest, device_info: Optional[DeviceInfo] = None) -> LoginResponse:
        """Authenticate user with email and password."""
        try:
            # Find user by email
            user = self.db.query(User).filter(User.email == login_data.email).first()
            if not user:
                raise ValueError("Invalid email or password")

            # Check if user is active
            if user.status != UserStatus.active:
                raise ValueError("Account is inactive or suspended")

            # Verify password
            if not self._verify_password(login_data.password, user.password_hash):
                raise ValueError("Invalid email or password")

            # Generate tokens
            access_token, refresh_token = self._generate_tokens(user, device_info)

            # Create response
            user_profile = UserProfileResponse(
                user_id=user.user_id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                phone=user.phone,
                profile_image=user.profile_image,
                email_verified=user.email_verified,
                phone_verified=user.phone_verified,
                role=user.role.value,
                status=user.status.value,
                created_at=user.created_at,
                updated_at=user.updated_at
            )

            tokens = {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'Bearer',
                'expires_in': self.jwt_expiration_hours * 3600
            }

            return LoginResponse(
                user=user_profile,
                tokens=tokens,
                is_new_user=False
            )

        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            raise

    def signup(self, signup_data: SignupRequest, device_info: Optional[DeviceInfo] = None) -> SignupResponse:
        """Register a new user."""
        try:
            # Check if user already exists
            existing_user = self.db.query(User).filter(User.email == signup_data.email).first()
            if existing_user:
                raise ValueError("User with this email already exists")

            existing_phone = self.db.query(User).filter(User.phone == signup_data.phone).first()
            if existing_phone:
                raise ValueError("User with this phone number already exists")

            # Hash password
            password_hash = self._hash_password(signup_data.password)

            # Create user
            user = User(
                email=signup_data.email,
                phone=signup_data.phone,
                password_hash=password_hash,
                first_name=signup_data.first_name,
                last_name=signup_data.last_name,
                role=UserRole.customer,  # Default role
                status=UserStatus.active,
                profile_image=None,
                email_verified=False,
                phone_verified=False
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)

            # Generate tokens
            access_token, refresh_token = self._generate_tokens(user, device_info)

            # Send OTP for phone verification
            self._send_otp(user.phone, OTPType.phone_verification, user.user_id)

            # Create response
            user_profile = UserProfileResponse(
                user_id=user.user_id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                phone=user.phone,
                profile_image=user.profile_image,
                email_verified=user.email_verified,
                phone_verified=user.phone_verified,
                role=user.role.value,
                status=user.status.value,
                created_at=user.created_at,
                updated_at=user.updated_at
            )

            tokens = {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'Bearer',
                'expires_in': self.jwt_expiration_hours * 3600
            }

            return SignupResponse(
                user=user_profile,
                tokens=tokens,
                requires_verification=True
            )

        except Exception as e:
            logger.error(f"Signup error: {str(e)}")
            raise

    def google_signin(self, google_data: GoogleSignInRequest, device_info: Optional[DeviceInfo] = None) -> GoogleSignInResponse:
        """Authenticate user with Google OAuth."""
        try:
            # Verify Google token
            google_user_info = self._verify_google_token(google_data.id_token)
            if not google_user_info:
                raise ValueError("Invalid Google token")

            # Check if user exists with this Google account
            oauth_provider = self.db.query(OAuthProvider).filter(
                OAuthProvider.provider == AuthProvider.google,
                OAuthProvider.provider_user_id == google_user_info.google_id
            ).first()

            if oauth_provider:
                # User exists, get user details
                user = self.db.query(User).filter(User.user_id == oauth_provider.user_id).first()
                if not user or user.status != UserStatus.active:
                    raise ValueError("Account is inactive or suspended")
            else:
                # Check if user exists with same email
                user = self.db.query(User).filter(User.email == google_user_info.email).first()
                
                if user:
                    # Link Google account to existing user
                    oauth_provider = OAuthProvider(
                        user_id=user.user_id,
                        provider=AuthProvider.google,
                        provider_user_id=google_user_info.google_id,
                        provider_email=google_user_info.email,
                        provider_name=google_user_info.name,
                        provider_photo_url=google_user_info.picture,
                        is_active=True
                    )
                    self.db.add(oauth_provider)
                else:
                    # Create new user
                    user = User(
                        email=google_user_info.email,
                        phone="",  # Will be filled later
                        password_hash="",  # No password for OAuth users
                        first_name=google_user_info.given_name,
                        last_name=google_user_info.family_name,
                        role=UserRole.customer,
                        status=UserStatus.active,
                        profile_image=google_user_info.picture,
                        email_verified=google_user_info.verified_email,
                        phone_verified=False
                    )
                    self.db.add(user)
                    self.db.commit()
                    self.db.refresh(user)

                    # Create OAuth provider record
                    oauth_provider = OAuthProvider(
                        user_id=user.user_id,
                        provider=AuthProvider.google,
                        provider_user_id=google_user_info.google_id,
                        provider_email=google_user_info.email,
                        provider_name=google_user_info.name,
                        provider_photo_url=google_user_info.picture,
                        is_active=True
                    )
                    self.db.add(oauth_provider)

                self.db.commit()

            # Generate tokens
            access_token, refresh_token = self._generate_tokens(user, device_info)

            # Create response
            user_profile = UserProfileResponse(
                user_id=user.user_id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                phone=user.phone,
                profile_image=user.profile_image,
                email_verified=user.email_verified,
                phone_verified=user.phone_verified,
                role=user.role.value,
                status=user.status.value,
                created_at=user.created_at,
                updated_at=user.updated_at
            )

            tokens = {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'Bearer',
                'expires_in': self.jwt_expiration_hours * 3600
            }

            return GoogleSignInResponse(
                user=user_profile,
                tokens=tokens,
                is_new_user=not oauth_provider,
                requires_verification=not user.phone_verified
            )

        except Exception as e:
            logger.error(f"Google signin error: {str(e)}")
            raise

    def refresh_token(self, refresh_data: RefreshTokenRequest) -> RefreshTokenResponse:
        """Refresh access token using refresh token."""
        try:
            # Find refresh token
            refresh_token_hash = self._hash_password(refresh_data.refresh_token)
            refresh_token_obj = self.db.query(RefreshToken).filter(
                RefreshToken.token_hash == refresh_token_hash,
                RefreshToken.is_revoked == False,
                RefreshToken.expires_at > datetime.utcnow()
            ).first()

            if not refresh_token_obj:
                raise ValueError("Invalid or expired refresh token")

            # Get user
            user = self.db.query(User).filter(User.user_id == refresh_token_obj.user_id).first()
            if not user or user.status != UserStatus.active:
                raise ValueError("User not found or inactive")

            # Generate new tokens
            access_token, new_refresh_token = self._generate_tokens(user)

            # Revoke old refresh token
            refresh_token_obj.is_revoked = True
            self.db.commit()

            return RefreshTokenResponse(
                access_token=access_token,
                refresh_token=new_refresh_token,
                token_type="Bearer",
                expires_in=self.jwt_expiration_hours * 3600
            )

        except Exception as e:
            logger.error(f"Refresh token error: {str(e)}")
            raise

    def _send_otp(self, phone: Optional[str], email: Optional[str], otp_type: OTPType, user_id: UUID) -> None:
        """Send OTP via SMS or email."""
        try:
            # Generate 6-digit OTP
            otp_code = str(secrets.randbelow(900000) + 100000)
            
            # Store OTP
            otp_obj = OTPVerification(
                user_id=user_id,
                phone=phone,
                email=email,
                otp_code=otp_code,
                otp_type=otp_type,
                expires_at=datetime.utcnow() + timedelta(minutes=5)  # OTP valid for 5 minutes
            )
            self.db.add(otp_obj)
            self.db.commit()

            # TODO: Integrate with SMS/Email service
            # For now, just log the OTP
            logger.info(f"OTP for {phone or email}: {otp_code}")

        except Exception as e:
            logger.error(f"Error sending OTP: {str(e)}")
            raise

    def send_otp(self, phone: Optional[str], email: Optional[str], otp_type: OTPType) -> OTPResponse:
        """Send OTP for verification."""
        try:
            # Find user
            user = None
            if phone:
                user = self.db.query(User).filter(User.phone == phone).first()
            elif email:
                user = self.db.query(User).filter(User.email == email).first()

            if not user:
                raise ValueError("User not found")

            # Send OTP
            self._send_otp(phone, email, otp_type, user.user_id)

            return OTPResponse(
                message="OTP sent successfully",
                expires_in=300,  # 5 minutes
                phone=phone,
                email=email
            )

        except Exception as e:
            logger.error(f"Send OTP error: {str(e)}")
            raise

    def verify_otp(self, verify_data: VerifyOTPRequest) -> VerifyOTPResponse:
        """Verify OTP code."""
        try:
            # Find OTP record
            query = self.db.query(OTPVerification).filter(
                OTPVerification.otp_code == verify_data.otp_code,
                OTPVerification.otp_type == verify_data.otp_type,
                OTPVerification.is_verified == False,
                OTPVerification.expires_at > datetime.utcnow()
            )

            if verify_data.phone:
                query = query.filter(OTPVerification.phone == verify_data.phone)
            elif verify_data.email:
                query = query.filter(OTPVerification.email == verify_data.email)

            otp_obj = query.first()

            if not otp_obj:
                raise ValueError("Invalid or expired OTP")

            # Check attempts
            if otp_obj.attempts >= otp_obj.max_attempts:
                raise ValueError("Maximum OTP attempts exceeded")

            # Verify OTP
            otp_obj.is_verified = True
            otp_obj.attempts += 1
            self.db.commit()

            # Update user verification status
            user = self.db.query(User).filter(User.user_id == otp_obj.user_id).first()
            if verify_data.otp_type == OTPType.phone_verification:
                user.phone_verified = True
            elif verify_data.otp_type == OTPType.email_verification:
                user.email_verified = True

            self.db.commit()

            return VerifyOTPResponse(
                verified=True,
                message="OTP verified successfully",
                requires_profile_completion=not user.phone or not user.email_verified
            )

        except Exception as e:
            logger.error(f"Verify OTP error: {str(e)}")
            raise

    def logout(self, user_id: UUID, logout_data: LogoutRequest) -> LogoutResponse:
        """Logout user and revoke tokens."""
        try:
            if logout_data.logout_all_devices:
                # Revoke all refresh tokens for user
                self.db.query(RefreshToken).filter(
                    RefreshToken.user_id == user_id
                ).update({"is_revoked": True})
                
                # Deactivate all sessions
                self.db.query(UserSession).filter(
                    UserSession.user_id == user_id
                ).update({"is_active": False})
                
                logged_out_devices = self.db.query(UserSession).filter(
                    UserSession.user_id == user_id
                ).count()
            else:
                # Revoke specific refresh token
                if logout_data.refresh_token:
                    refresh_token_hash = self._hash_password(logout_data.refresh_token)
                    self.db.query(RefreshToken).filter(
                        RefreshToken.token_hash == refresh_token_hash,
                        RefreshToken.user_id == user_id
                    ).update({"is_revoked": True})
                
                logged_out_devices = 1

            self.db.commit()

            return LogoutResponse(
                message="Logged out successfully",
                logged_out_devices=logged_out_devices
            )

        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            raise

    def get_user_sessions(self, user_id: UUID) -> UserSessionsResponse:
        """Get all active sessions for user."""
        try:
            sessions = self.db.query(UserSession).filter(
                UserSession.user_id == user_id,
                UserSession.is_active == True
            ).order_by(UserSession.last_activity.desc()).all()

            session_list = []
            for session in sessions:
                session_list.append({
                    'session_id': session.session_id,
                    'device_name': session.device_name,
                    'device_type': session.device_type.value if session.device_type else None,
                    'platform': session.platform.value if session.platform else None,
                    'app_version': session.app_version,
                    'last_activity': session.last_activity,
                    'is_current': False  # This would need to be determined based on current session
                })

            return UserSessionsResponse(
                sessions=session_list,
                total_sessions=len(session_list)
            )

        except Exception as e:
            logger.error(f"Get user sessions error: {str(e)}")
            raise
