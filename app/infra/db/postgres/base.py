from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from app.config.config import DATABASE_URL  # Import from your config module
from app.config.logger import get_logger
import traceback

try:
    # Create the SQLAlchemy engine using the database URL from the config
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

    # Create a scoped session for thread-safety
    SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
except Exception as e:
    logger = get_logger(__name__)
    logger.error(f"Error connecting to database: {str(e)}")
    logger.error(traceback.format_exc())
    
    # Create a dummy engine and session for testing
    from sqlalchemy.pool import NullPool
    engine = create_engine('sqlite:///:memory:', poolclass=NullPool)
    SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Create a base class for your ORM models
Base = declarative_base()
