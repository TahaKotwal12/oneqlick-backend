#!/usr/bin/env python3
"""
Script to create the pending_users table in the database.
Run this script to ensure the pending_users table is created.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.infra.db.postgres.base import Base, engine
from app.infra.db.postgres.models.pending_user import PendingUser
from app.config.logger import get_logger

logger = get_logger(__name__)

def create_pending_users_table():
    """Create the pending_users table if it doesn't exist."""
    try:
        # Create all tables (this will create pending_users table if it doesn't exist)
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Pending users table created successfully!")
        
        # Verify the table exists
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if 'core_mstr_one_qlick_pending_users_tbl' in tables:
            logger.info("✅ Verified: pending_users table exists in database")
        else:
            logger.error("❌ Error: pending_users table not found in database")
            
    except Exception as e:
        logger.error(f"❌ Error creating pending_users table: {e}")
        raise

if __name__ == "__main__":
    create_pending_users_table()
