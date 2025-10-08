#!/usr/bin/env python3
"""
Test script for batch cleanup functionality

This script tests the batch cleanup service without actually deleting data.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.batch_cleanup_service import BatchCleanupService
from app.config.logger import get_logger

logger = get_logger(__name__)


def test_duplicate_email_detection():
    """Test the duplicate email detection functionality."""
    logger.info("Testing duplicate email detection...")
    
    cleanup_service = BatchCleanupService()
    
    try:
        # Test the duplicate email detection by running a dry cleanup
        logger.info("Running dry cleanup to detect duplicates...")
        duplicate_count = cleanup_service.run_dry_cleanup()
        logger.info(f"Found {duplicate_count} records that would be deleted")
        
        return duplicate_count
        
    except Exception as e:
        logger.error(f"Error testing duplicate email detection: {str(e)}")
        return 0


def test_cleanup_service_status():
    """Test the cleanup service status functionality."""
    logger.info("Testing cleanup service status...")
    
    cleanup_service = BatchCleanupService()
    status = cleanup_service.get_status()
    
    logger.info(f"Service status: {status}")
    return status


def main():
    """Main test function."""
    logger.info("Starting batch cleanup tests...")
    
    try:
        # Test 1: Service status
        test_cleanup_service_status()
        
        # Test 2: Duplicate email detection (dry run)
        duplicate_count = test_duplicate_email_detection()
        
        logger.info(f"Test completed. Found {duplicate_count} duplicate emails.")
        
        if duplicate_count > 0:
            logger.info("To run actual cleanup, use: python batch_cleanup.py --run-once")
        else:
            logger.info("No duplicate emails found. Database is clean.")
            
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
