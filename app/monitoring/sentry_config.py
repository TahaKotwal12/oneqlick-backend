"""
Sentry configuration for OneQlick Backend
Provides error tracking and performance monitoring
"""

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
import os
import logging

logger = logging.getLogger(__name__)


def init_sentry():
    """
    Initialize Sentry for error tracking and performance monitoring.
    
    Features:
    - Error tracking with stack traces
    - Performance monitoring (API endpoints, database queries)
    - Release tracking
    - Environment-based configuration
    """
    sentry_dsn = os.getenv("SENTRY_DSN", "")
    environment = os.getenv("SENTRY_ENVIRONMENT", os.getenv("APP_ENV", "production"))
    
    if not sentry_dsn:
        logger.warning("⚠️ SENTRY_DSN not set, skipping Sentry initialization")
        logger.info("To enable Sentry: Set SENTRY_DSN in .env file")
        return
    
    try:
        # Get configuration from environment
        traces_sample_rate = float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "1.0"))
        profiles_sample_rate = float(os.getenv("SENTRY_PROFILES_SAMPLE_RATE", "1.0"))
        
        # Initialize Sentry
        sentry_sdk.init(
            dsn=sentry_dsn,
            environment=environment,
            
            # Performance Monitoring
            traces_sample_rate=traces_sample_rate,  # 1.0 = 100% of transactions
            profiles_sample_rate=profiles_sample_rate,  # 1.0 = 100% profiling
            
            # Integrations
            integrations=[
                # FastAPI integration - automatic request tracking
                FastApiIntegration(
                    transaction_style="endpoint",  # Group by endpoint, not URL
                ),
                
                # SQLAlchemy integration - track database queries
                SqlalchemyIntegration(),
                
                # Redis integration - track Redis operations
                RedisIntegration(),
                
                # Logging integration - capture logs as breadcrumbs
                LoggingIntegration(
                    level=logging.INFO,  # Capture info and above
                    event_level=logging.ERROR  # Send errors as events
                ),
            ],
            
            # Release tracking (for deployment tracking)
            release=os.getenv("SENTRY_RELEASE", os.getenv("APP_VERSION", "1.0.0")),
            
            # Additional options
            attach_stacktrace=True,  # Attach stack traces to all events
            send_default_pii=False,  # Don't send personally identifiable information
            
            # Performance monitoring options
            _experiments={
                "profiles_sample_rate": profiles_sample_rate,
            },
            
            # Custom tags
            tags={
                "service": "oneqlick-backend",
                "platform": "fastapi",
            },
            
            # Before send hook - filter sensitive data
            before_send=before_send_hook,
        )
        
        logger.info(f"✅ Sentry initialized successfully")
        logger.info(f"   Environment: {environment}")
        logger.info(f"   Traces sample rate: {traces_sample_rate * 100}%")
        logger.info(f"   Profiles sample rate: {profiles_sample_rate * 100}%")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize Sentry: {e}")
        logger.warning("Continuing without Sentry monitoring")


def before_send_hook(event, hint):
    """
    Filter sensitive data before sending to Sentry.
    
    This hook is called before every event is sent to Sentry.
    Use it to remove sensitive information like passwords, tokens, etc.
    """
    # Remove sensitive headers
    if 'request' in event and 'headers' in event['request']:
        headers = event['request']['headers']
        sensitive_headers = ['authorization', 'cookie', 'x-api-key']
        
        for header in sensitive_headers:
            if header in headers:
                headers[header] = '[Filtered]'
    
    # Remove sensitive environment variables
    if 'contexts' in event and 'runtime' in event['contexts']:
        runtime = event['contexts']['runtime']
        if 'env' in runtime:
            sensitive_env_vars = [
                'DATABASE_URL', 'REDIS_PASSWORD', 'JWT_SECRET_KEY',
                'SECRET_KEY', 'SENTRY_DSN', 'RAZORPAY_KEY_SECRET'
            ]
            for var in sensitive_env_vars:
                if var in runtime['env']:
                    runtime['env'][var] = '[Filtered]'
    
    return event


def capture_exception(exception: Exception, **kwargs):
    """
    Manually capture an exception to Sentry.
    
    Usage:
        try:
            risky_operation()
        except Exception as e:
            capture_exception(e, extra={"user_id": user.id})
            raise
    """
    sentry_sdk.capture_exception(exception, **kwargs)


def capture_message(message: str, level: str = "info", **kwargs):
    """
    Manually capture a message to Sentry.
    
    Usage:
        capture_message("Payment gateway timeout", level="warning", extra={"order_id": order.id})
    """
    sentry_sdk.capture_message(message, level=level, **kwargs)


def set_user_context(user_id: str = None, email: str = None, **kwargs):
    """
    Set user context for Sentry events.
    
    Usage:
        set_user_context(user_id=str(user.id), email=user.email, role=user.role)
    """
    user_data = {}
    if user_id:
        user_data['id'] = user_id
    if email:
        user_data['email'] = email
    user_data.update(kwargs)
    
    sentry_sdk.set_user(user_data)


def set_context(key: str, value: dict):
    """
    Set custom context for Sentry events.
    
    Usage:
        set_context("order", {"order_id": order.id, "total": order.total})
    """
    sentry_sdk.set_context(key, value)


def add_breadcrumb(message: str, category: str = "default", level: str = "info", **data):
    """
    Add a breadcrumb to track user actions.
    
    Usage:
        add_breadcrumb("User searched for restaurants", category="search", query="pizza")
    """
    sentry_sdk.add_breadcrumb(
        message=message,
        category=category,
        level=level,
        data=data
    )
