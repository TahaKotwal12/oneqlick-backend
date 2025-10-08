"""
Batch Cleanup Service for Unverified Users

This service runs periodically to clean up unverified users from the pending_users table
if they already exist in the main users table with the same email address.
"""

import threading
import time
from datetime import datetime, timedelta
from typing import List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, delete
from app.infra.db.postgres.postgres_config import SessionLocal
from app.infra.db.postgres.models.user import User
from app.infra.db.postgres.models.pending_user import PendingUser
from app.config.logger import get_logger

logger = get_logger(__name__)


class BatchCleanupService:
    """Service to clean up unverified users who exist in main user table."""
    
    def __init__(self, interval_hours: int = 1):
        """
        Initialize the batch cleanup service.
        
        Args:
            interval_hours (int): Hours between cleanup runs. Default is 1 hour.
        """
        self.interval_hours = interval_hours
        self.interval_seconds = interval_hours * 3600
        self.running = False
        self.thread = None
        
    def start(self):
        """Start the batch cleanup service in a separate thread."""
        if self.running:
            logger.warning("Batch cleanup service is already running")
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._run_cleanup_loop, daemon=True)
        self.thread.start()
        logger.info(f"Batch cleanup service started with {self.interval_hours} hour interval")
        
    def stop(self):
        """Stop the batch cleanup service."""
        if not self.running:
            logger.warning("Batch cleanup service is not running")
            return
            
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Batch cleanup service stopped")
        
    def _run_cleanup_loop(self):
        """Main loop for the cleanup service."""
        while self.running:
            try:
                logger.info("Starting batch cleanup of unverified users")
                deleted_count = self.cleanup_unverified_users()
                logger.info(f"Batch cleanup completed. Deleted {deleted_count} unverified user records")
                
            except Exception as e:
                logger.error(f"Error during batch cleanup: {str(e)}")
                
            # Wait for the specified interval
            time.sleep(self.interval_seconds)
            
    def cleanup_unverified_users(self, dry_run: bool = False) -> int:
        """
        Clean up unverified users who exist in the main user table.
        
        Args:
            dry_run (bool): If True, only count records without deleting them
        
        Returns:
            int: Number of records deleted (or would be deleted in dry run)
        """
        db = SessionLocal()
        deleted_count = 0
        
        try:
            # Find pending users whose email exists in the main users table
            duplicate_emails = self._find_duplicate_emails(db)
            
            if not duplicate_emails:
                logger.info("No duplicate emails found between pending and main users")
                return 0
                
            logger.info(f"Found {len(duplicate_emails)} duplicate emails to clean up")
            
            # Delete pending users with duplicate emails (or count them in dry run)
            for email in duplicate_emails:
                try:
                    if dry_run:
                        # Count records that would be deleted
                        count = db.query(PendingUser).filter(PendingUser.email == email).count()
                        deleted_count += count
                        logger.debug(f"Would delete {count} pending user(s) with email: {email}")
                    else:
                        # Delete from pending users table
                        result = db.execute(
                            delete(PendingUser).where(PendingUser.email == email)
                        )
                        deleted_count += result.rowcount
                        logger.debug(f"Deleted pending user with email: {email}")
                    
                except Exception as e:
                    logger.error(f"Error processing pending user with email {email}: {str(e)}")
                    continue
                    
            # Commit the transaction only if not dry run
            if not dry_run:
                db.commit()
                logger.info(f"Successfully deleted {deleted_count} unverified user records")
            else:
                logger.info(f"Dry run: Would delete {deleted_count} unverified user records")
            
        except Exception as e:
            logger.error(f"Error during cleanup process: {str(e)}")
            db.rollback()
            raise
            
        finally:
            db.close()
            
        return deleted_count
        
    def _find_duplicate_emails(self, db: Session) -> List[str]:
        """
        Find emails that exist in both pending users and main users tables.
        
        Args:
            db (Session): Database session
            
        Returns:
            List[str]: List of duplicate email addresses
        """
        try:
            # Query to find emails that exist in both tables
            query = db.query(PendingUser.email).join(
                User, PendingUser.email == User.email
            ).distinct()
            
            duplicate_emails = [row[0] for row in query.all()]
            return duplicate_emails
            
        except Exception as e:
            logger.error(f"Error finding duplicate emails: {str(e)}")
            return []
            
    def run_cleanup_now(self) -> int:
        """
        Run cleanup immediately (for testing or manual execution).
        
        Returns:
            int: Number of records deleted
        """
        logger.info("Running immediate cleanup of unverified users")
        return self.cleanup_unverified_users()
        
    def run_dry_cleanup(self) -> int:
        """
        Run cleanup in dry run mode (count records without deleting).
        
        Returns:
            int: Number of records that would be deleted
        """
        logger.info("Running dry cleanup of unverified users")
        return self.cleanup_unverified_users(dry_run=True)
        
    def get_status(self) -> dict:
        """
        Get the current status of the batch cleanup service.
        
        Returns:
            dict: Status information
        """
        return {
            "running": self.running,
            "interval_hours": self.interval_hours,
            "thread_alive": self.thread.is_alive() if self.thread else False
        }


# Global instance for the application
batch_cleanup_service = BatchCleanupService(interval_hours=1)


def start_batch_cleanup():
    """Start the batch cleanup service."""
    batch_cleanup_service.start()


def stop_batch_cleanup():
    """Stop the batch cleanup service."""
    batch_cleanup_service.stop()


def run_cleanup_now():
    """Run cleanup immediately."""
    return batch_cleanup_service.run_cleanup_now()


def get_cleanup_status():
    """Get cleanup service status."""
    return batch_cleanup_service.get_status()
