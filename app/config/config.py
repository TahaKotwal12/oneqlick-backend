from dotenv import load_dotenv
import os
import logging

# Load .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database Configuration - Neon PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://neondb_owner:npg_WU6NjGwae1bh@ep-cold-thunder-ad7m6qy2-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')

# Database pool configuration
DB_POOL_MAX_SIZE = int(os.getenv("DB_POOL_MAX_SIZE", "10"))
DB_POOL_MIN_IDLE = int(os.getenv("DB_POOL_MIN_IDLE", "1"))
DB_POOL_IDLE_TIMEOUT = int(os.getenv("DB_POOL_IDLE_TIMEOUT", "30000"))
DB_POOL_MAX_LIFETIME = int(os.getenv("DB_POOL_MAX_LIFETIME", "1800000"))
DB_POOL_CONNECTION_TIMEOUT = int(os.getenv("DB_POOL_CONNECTION_TIMEOUT", "30000"))
DB_POOL_NAME = os.getenv("DB_POOL_NAME", "OneQlickFoodDeliveryCP")

# Redis Configuration for caching and sessions
REDIS_CONFIG = {
    "host": os.getenv("REDIS_HOST", "localhost"),
    "port": int(os.getenv("REDIS_PORT", 6379)),
    "password": os.getenv("REDIS_PASSWORD", ""),
    "ttl": int(os.getenv("REDIS_TTL", 300)),
    "namespace": os.getenv("REDIS_NAMESPACE", "oneqlick"),
    "timeout": int(os.getenv("REDIS_TIMEOUT_MS", 10000)),
    "pool": {
        "max_active": int(os.getenv("REDIS_MAX_ACTIVE", 20)),
        "max_idle": int(os.getenv("REDIS_MAX_IDLE", 5)),
        "min_idle": int(os.getenv("REDIS_MIN_IDLE", 1))
    }
}

# Application Configuration
APP_ENV = os.getenv("APP_ENV", "development")
SECRET_KEY = os.getenv("SECRET_KEY", "oneqlick-secret-key-2024-production-ready")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "debug").upper()

# CORS Configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8081").split(",")
CORS_METHODS = os.getenv("CORS_METHODS", "GET,POST,PUT,DELETE,OPTIONS").split(",")
CORS_HEADERS = os.getenv("CORS_HEADERS", "*").split(",")

# JWT Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "oneqlick-jwt-secret-key-2024-production-ready")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

# Payment Configuration (for future implementation)
PAYMENT_CONFIG = {
    "razorpay_key_id": os.getenv("RAZORPAY_KEY_ID", ""),
    "razorpay_key_secret": os.getenv("RAZORPAY_KEY_SECRET", ""),
    "paytm_merchant_id": os.getenv("PAYTM_MERCHANT_ID", ""),
    "paytm_merchant_key": os.getenv("PAYTM_MERCHANT_KEY", "")
}

# SMS/Notification Configuration (for OTP and notifications)
NOTIFICATION_CONFIG = {
    "sms_provider": os.getenv("SMS_PROVIDER", "twilio"),  # or "msg91"
    "twilio_account_sid": os.getenv("TWILIO_ACCOUNT_SID", ""),
    "twilio_auth_token": os.getenv("TWILIO_AUTH_TOKEN", ""),
    "twilio_phone_number": os.getenv("TWILIO_PHONE_NUMBER", ""),
    "msg91_auth_key": os.getenv("MSG91_AUTH_KEY", ""),
    "msg91_template_id": os.getenv("MSG91_TEMPLATE_ID", "")
}

# Google OAuth Configuration
GOOGLE_OAUTH_CONFIG = {
    "client_id": os.getenv("GOOGLE_CLIENT_ID", "1024710005377-603b3r4u26tgehu0nc1d9frjb1j0v1u9.apps.googleusercontent.com"),
    "client_secret": os.getenv("GOOGLE_CLIENT_SECRET", ""),
    "project_id": os.getenv("GOOGLE_PROJECT_ID", "pragmatic-braid-445409-h4"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs"
}

# Security Configuration
SECURITY_CONFIG = {
    "bcrypt_rounds": int(os.getenv("BCRYPT_ROUNDS", "12")),
    "password_min_length": int(os.getenv("PASSWORD_MIN_LENGTH", "8")),
    "password_require_uppercase": os.getenv("PASSWORD_REQUIRE_UPPERCASE", "true").lower() == "true",
    "password_require_lowercase": os.getenv("PASSWORD_REQUIRE_LOWERCASE", "true").lower() == "true",
    "password_require_numbers": os.getenv("PASSWORD_REQUIRE_NUMBERS", "true").lower() == "true",
    "password_require_special_chars": os.getenv("PASSWORD_REQUIRE_SPECIAL_CHARS", "true").lower() == "true",
}

# File Upload Configuration
UPLOAD_CONFIG = {
    "max_size": int(os.getenv("UPLOAD_MAX_SIZE", "10485760")),  # 10MB
    "allowed_extensions": os.getenv("ALLOWED_EXTENSIONS", "jpg,jpeg,png,gif,pdf,doc,docx").split(","),
    "upload_path": os.getenv("UPLOAD_PATH", "uploads"),
}

# Rate Limiting Configuration
RATE_LIMIT_CONFIG = {
    "requests": int(os.getenv("RATE_LIMIT_REQUESTS", "100")),
    "window": int(os.getenv("RATE_LIMIT_WINDOW", "3600")),  # 1 hour
}

# Email Configuration
EMAIL_CONFIG = {
    "provider": os.getenv("EMAIL_PROVIDER", "smtp"),
    "smtp_host": os.getenv("SMTP_HOST", ""),
    "smtp_port": int(os.getenv("SMTP_PORT", "587")),
    "smtp_username": os.getenv("SMTP_USERNAME", ""),
    "smtp_password": os.getenv("SMTP_PASSWORD", ""),
    "smtp_use_tls": os.getenv("SMTP_USE_TLS", "true").lower() == "true",
}

# Monitoring Configuration
MONITORING_CONFIG = {
    "sentry_dsn": os.getenv("SENTRY_DSN", ""),
    "log_file_path": os.getenv("LOG_FILE_PATH", "logs/app.log"),
    "log_max_size": int(os.getenv("LOG_MAX_SIZE", "10485760")),  # 10MB
    "log_backup_count": int(os.getenv("LOG_BACKUP_COUNT", "5")),
}

# Development Configuration
DEV_CONFIG = {
    "reload": os.getenv("RELOAD", "true").lower() == "true",
    "host": os.getenv("HOST", "0.0.0.0"),
    "port": int(os.getenv("PORT", "8000")),
    "workers": int(os.getenv("WORKERS", "1")),
}

# Configuration validation
def validate_config():
    """Validate critical configuration values"""
    errors = []
    
    if SECRET_KEY == "your-secret-key-change-in-production":
        errors.append("SECRET_KEY must be changed from default value")
    
    if JWT_SECRET_KEY == "your-jwt-secret-key":
        errors.append("JWT_SECRET_KEY must be changed from default value")
    
    if APP_ENV == "production" and DEBUG:
        errors.append("DEBUG should be False in production")
    
    if errors:
        logger.warning("Configuration validation warnings:")
        for error in errors:
            logger.warning(f"  - {error}")
    
    return len(errors) == 0

# Validate configuration on import
validate_config()
