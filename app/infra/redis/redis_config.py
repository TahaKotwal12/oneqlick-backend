import redis
import os
from app.config.logger import get_logger

logger = get_logger(__name__)

def get_redis_client() -> redis.Redis:
    """Get Redis client instance."""
    try:
        # Get Redis configuration from environment variables
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', 6379))
        redis_db = int(os.getenv('REDIS_DB', 0))
        redis_password = os.getenv('REDIS_PASSWORD', None)
        
        # Create Redis client configuration
        redis_config = {
            'host': redis_host,
            'port': redis_port,
            'db': redis_db,
            'decode_responses': True,  # Automatically decode responses to strings
            'socket_connect_timeout': 5,
            'socket_timeout': 5,
            'retry_on_timeout': True
        }
        
        # Only add password if it's provided
        if redis_password:
            redis_config['password'] = redis_password
        
        # Create Redis client
        redis_client = redis.Redis(**redis_config)
        
        # Test connection
        redis_client.ping()
        logger.info(f"Redis connected successfully to {redis_host}:{redis_port}")
        
        return redis_client
        
    except redis.AuthenticationError as e:
        logger.error(f"Redis authentication error: {str(e)}")
        logger.error("Please check your REDIS_PASSWORD environment variable or Redis configuration")
        raise
    except redis.ConnectionError as e:
        logger.error(f"Redis connection error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error initializing Redis client: {str(e)}")
        raise

def get_redis_client_sync() -> redis.Redis:
    """Get synchronous Redis client instance."""
    return get_redis_client() 