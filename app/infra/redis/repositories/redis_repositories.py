import redis
from typing import Any, Optional, Dict, List
import json
from app.config.config import REDIS_CONFIG
from app.config.logger import get_logger
import traceback

logger = get_logger(__name__)

class RedisRepository:
    """
    Repository class for Redis operations
    """
    _instance = None
    _redis_client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisRepository, cls).__new__(cls)
            cls._instance._initialize_redis_client()
        return cls._instance

    def _initialize_redis_client(self):
        """Initialize the Redis client with configuration from config.py"""
        try:
            # Print the REDIS_CONFIG for debugging
            logger.info(f"REDIS_CONFIG: {REDIS_CONFIG}")

            # Check if TLS is enabled (for Upstash and other cloud Redis services)
            use_tls = REDIS_CONFIG.get("use_tls", False)
            
            # Prepare connection parameters
            connection_params = {
                "host": REDIS_CONFIG["host"],
                "port": REDIS_CONFIG["port"],
                "password": REDIS_CONFIG["password"] if REDIS_CONFIG["password"] else None,
                "socket_timeout": REDIS_CONFIG["timeout"] / 1000,  # Convert ms to seconds
                "socket_connect_timeout": 5,  # 5 second connection timeout
                "decode_responses": True,
                "retry_on_timeout": True,
                "health_check_interval": 30,  # Health check every 30 seconds
            }
            
            # Add TLS/SSL parameters if enabled (for Upstash, Redis Cloud, etc.)
            if use_tls:
                logger.info("Enabling TLS/SSL for Redis connection (Upstash/Cloud Redis)")
                connection_params["ssl"] = True
                connection_params["ssl_cert_reqs"] = None  # Don't verify SSL certificates
                # Alternative: Use ssl_cert_reqs="required" with ssl_ca_certs for production
            
            self._redis_client = redis.Redis(**connection_params)
            
            # Test the connection with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    self._redis_client.ping()
                    logger.info(f"Successfully connected to Redis (TLS: {use_tls})")
                    break
                except redis.ConnectionError as e:
                    if attempt < max_retries - 1:
                        logger.warning(f"Redis connection attempt {attempt + 1} failed, retrying...")
                        import time
                        time.sleep(1)
                    else:
                        raise
                        
        except Exception as e:
            logger.error(f"Failed to initialize Redis client: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            self._redis_client = None
            raise


    def delete_pattern(self, key_prefix: str) -> int:
        """
        Delete keys matching a pattern using SCAN for efficiency
        """
        pattern = f"{key_prefix}*"
        logger.info(f"Deleting keys with key_prefix: {key_prefix}")
        try:
            if self._redis_client is None:
                self._initialize_redis_client()
            logger.info(f"Deleting keys with pattern: {pattern}")
            cursor = 0
            total_deleted = 0
            while True:
                cursor, keys = self._redis_client.scan(cursor=cursor, match=pattern, count=1000)
                if keys:
                    deleted = self._redis_client.delete(*keys)
                    total_deleted += deleted
                    logger.info(f"Deleted {deleted} keys in this batch.")
                if cursor == 0:
                    break
            logger.info(f"Total keys deleted for pattern {pattern}: {total_deleted}")
            return total_deleted
        except Exception as e:
            logger.error(f"Error deleting Redis keys with pattern {pattern}: {str(e)}\n{traceback.format_exc()}")
            return 0
