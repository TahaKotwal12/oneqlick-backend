from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
from app.config.config import (
    DATABASE_URL,
    DB_POOL_MAX_SIZE,
    DB_POOL_MIN_IDLE,
    DB_POOL_IDLE_TIMEOUT,
    DB_POOL_MAX_LIFETIME,
    DB_POOL_CONNECTION_TIMEOUT,
    DB_POOL_NAME
)
from app.config.logger import get_logger

try:
    engine = create_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        pool_size=DB_POOL_MAX_SIZE,
        max_overflow=DB_POOL_MIN_IDLE,
        pool_timeout=DB_POOL_CONNECTION_TIMEOUT / 1000,  # Convert from ms to seconds
        pool_recycle=DB_POOL_MAX_LIFETIME / 1000,  # Convert from ms to seconds
        pool_pre_ping=True,
        connect_args={"application_name": DB_POOL_NAME}
    )
    
    SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    
    logger = get_logger(__name__)
    logger.info("Supabase PostgreSQL database engine created successfully")
    
except Exception as e:
    logger = get_logger(__name__)
    logger.error(f"Failed to create database engine: {e}")
    raise e  # Re-raise the exception instead of falling back to SQLite

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
