import ssl
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
            ssl_enabled = REDIS_CONFIG["ssl"]["enabled"]
            ssl_params = {}
            
            if ssl_enabled:
                ssl_params = {
                    "ssl_ca_certs": REDIS_CONFIG["ssl"]["ca_certification_path"]
                }

            self._redis_client = redis.Redis(
                host=REDIS_CONFIG["host"],
                port=REDIS_CONFIG["port"],
                password=REDIS_CONFIG["password"],
                socket_timeout=REDIS_CONFIG["timeout"] / 1000,  # Convert ms to seconds
                ssl=ssl_enabled,
                ssl_cert_reqs=ssl.CERT_NONE,
                decode_responses=True
            )
            
            # Test the connection
            self._redis_client.ping()
            logger.info("Successfully connected to Redis")
        except Exception as e:
            logger.error(f"Failed to initialize Redis client: {str(e)}")
            self._redis_client = None
            raise


    def delete_pattern(self, keyPrefix: str) -> int:
        """
        Delete keys matching a pattern using SCAN for efficiency
        """
        pattern = f"{keyPrefix}*"
        logger.info(f"Deleting keys with keyPrefix: {keyPrefix}")
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
