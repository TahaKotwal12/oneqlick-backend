#!/usr/bin/env python3
"""
Demo script for batch cleanup functionality

This script demonstrates how the batch cleanup system works.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.batch_cleanup_service import BatchCleanupService
from app.config.logger import get_logger

logger = get_logger(__name__)


def demo_cleanup_service():
    """Demonstrate the batch cleanup service functionality."""
    print("=" * 60)
    print("BATCH CLEANUP SERVICE DEMO")
    print("=" * 60)
    
    # Create cleanup service
    cleanup_service = BatchCleanupService(interval_hours=1)
    
    # Show service status
    print("\n1. Service Status:")
    status = cleanup_service.get_status()
    print(f"   Running: {status['running']}")
    print(f"   Interval: {status['interval_hours']} hours")
    print(f"   Thread Alive: {status['thread_alive']}")
    
    # Run dry cleanup to see what would be deleted
    print("\n2. Dry Run - Checking for duplicate emails:")
    try:
        duplicate_count = cleanup_service.run_dry_cleanup()
        print(f"   Found {duplicate_count} records that would be deleted")
        
        if duplicate_count > 0:
            print("   These are unverified users whose emails already exist in the main users table.")
        else:
            print("   No duplicate emails found. Database is clean!")
            
    except Exception as e:
        print(f"   Error during dry run: {str(e)}")
        return
    
    # Show how to run actual cleanup
    print("\n3. To run actual cleanup:")
    print("   python batch_cleanup.py --run-once")
    print("   python batch_cleanup.py --daemon --interval 1")
    
    # Show how to integrate with main app
    print("\n4. To integrate with main application:")
    print("   from app.workers.batch_cleanup_worker import start_batch_cleanup_worker")
    print("   start_batch_cleanup_worker()")
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETED")
    print("=" * 60)


def main():
    """Main demo function."""
    try:
        demo_cleanup_service()
    except Exception as e:
        logger.error(f"Demo failed: {str(e)}")
        print(f"\nError: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
